"""
위클리 해축 MCP 서버
실시간 웹 검색 기반 축구 정보 제공
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List
import os
from datetime import datetime, timedelta

app = FastAPI(title="위클리 해축 MCP")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP 요청 모델
class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Any
    method: str
    params: Dict[str, Any] = {}

# 지원 리그 목록
SUPPORTED_LEAGUES = [
    "프리미어리그", "EPL", "Premier League",
    "세리에A", "Serie A",
    "라리가", "La Liga",
    "분데스리가", "Bundesliga",
    "사우디프로리그", "Saudi Pro League",
    "K리그1", "K League 1",
    "J리그", "J League",
    "MLS"
]

# 도구 정의
TOOLS = [
    {
        "name": "get_recent_matches",
        "description": "지난 7일간의 특정 리그 경기 결과를 웹 검색으로 조회합니다. 날짜, 팀명, 스코어, 주요 득점자를 포함합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "리그명 (프리미어리그, 세리에A, 라리가, 분데스리가, 사우디프로리그, K리그1, J리그, MLS)"
                },
                "team": {
                    "type": "string",
                    "description": "(선택) 특정 팀의 경기만 조회"
                }
            },
            "required": ["league"]
        }
    },
    {
        "name": "get_upcoming_matches",
        "description": "다음 7일간의 특정 리그 경기 일정을 웹 검색으로 조회합니다. 날짜, 시간, 대진 카드를 포함합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "리그명"
                },
                "team": {
                    "type": "string",
                    "description": "(선택) 특정 팀의 일정만 조회"
                }
            },
            "required": ["league"]
        }
    },
    {
        "name": "get_player_info",
        "description": "선수 이름을 입력하면 소속팀, 경력, 포지션, 골/어시스트, 수상 이력, 연봉 등을 웹 검색으로 조회합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "선수 이름 (예: 손흥민, 음바페, 호날두)"
                },
                "include_stats": {
                    "type": "boolean",
                    "description": "이번 시즌 상세 통계 포함 여부",
                    "default": True
                }
            },
            "required": ["player_name"]
        }
    },
    {
        "name": "get_league_standings",
        "description": "특정 리그의 현재 순위표를 웹 검색으로 조회합니다. 순위, 팀명, 경기수, 승점, 득실차를 포함합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "리그명"
                },
                "top_n": {
                    "type": "integer",
                    "description": "상위 몇 팀까지 조회 (기본: 전체)",
                    "default": 20
                }
            },
            "required": ["league"]
        }
    },
    {
        "name": "get_league_info",
        "description": "특정 리그의 역사, 참가팀 수, 시즌 정보, 우승 기록 등을 웹 검색으로 조회합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "리그명"
                }
            },
            "required": ["league"]
        }
    },
    {
        "name": "get_team_info",
        "description": "특정 팀의 정보(감독, 홈구장, 최근 성적, 주요 선수)를 웹 검색으로 조회합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "팀 이름 (예: 맨체스터 시티, 토트넘, 바르셀로나)"
                },
                "league": {
                    "type": "string",
                    "description": "(선택) 소속 리그"
                }
            },
            "required": ["team_name"]
        }
    },
    {
        "name": "get_top_scorers",
        "description": "특정 리그의 득점왕 순위를 웹 검색으로 조회합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "리그명"
                },
                "top_n": {
                    "type": "integer",
                    "description": "상위 몇 명까지 조회 (기본: 10명)",
                    "default": 10
                }
            },
            "required": ["league"]
        }
    },
    {
        "name": "compare_players",
        "description": "두 선수의 통계를 비교합니다. 골, 어시스트, 평점 등을 웹 검색으로 조회하여 비교합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "player1": {
                    "type": "string",
                    "description": "첫 번째 선수 이름"
                },
                "player2": {
                    "type": "string",
                    "description": "두 번째 선수 이름"
                },
                "season": {
                    "type": "string",
                    "description": "(선택) 시즌 (예: 2024-25, 기본: 현재 시즌)",
                    "default": "2024-25"
                }
            },
            "required": ["player1", "player2"]
        }
    },
    {
        "name": "get_transfer_news",
        "description": "최근 7일간의 이적 소식과 루머를 웹 검색으로 조회합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "(선택) 특정 리그의 이적 소식만 조회"
                },
                "team": {
                    "type": "string",
                    "description": "(선택) 특정 팀의 이적 소식만 조회"
                }
            }
        }
    }
]


# 도구 실행 함수
async def execute_tool(name: str, args: Dict) -> str:
    """각 도구의 로직을 실행하고 웹 검색 요청을 생성"""
    
    try:
        if name == "get_recent_matches":
            league = args.get("league", "")
            team = args.get("team", "")
            
            today = datetime.now()
            week_ago = today - timedelta(days=7)
            
            search_query = f"{league} 경기 결과 {week_ago.strftime('%Y년 %m월 %d일')} ~ {today.strftime('%Y년 %m월 %d일')}"
            if team:
                search_query += f" {team}"
            
            return f"""🔍 웹 검색이 필요합니다:

**검색 키워드**: {search_query}

**찾아야 할 정보**:
1. 날짜별 경기 결과
2. 홈팀 vs 원정팀
3. 최종 스코어
4. 주요 득점자 및 시간
5. 경기 하이라이트

다음 형식으로 정리해주세요:
📅 [날짜] 
   🏟️ [홈팀] {스코어} [원정팀]
   ⚽ 득점: [선수명(시간)]
"""

        elif name == "get_upcoming_matches":
            league = args.get("league", "")
            team = args.get("team", "")
            
            today = datetime.now()
            week_later = today + timedelta(days=7)
            
            search_query = f"{league} 경기 일정 {today.strftime('%Y년 %m월 %d일')} ~ {week_later.strftime('%Y년 %m월 %d일')}"
            if team:
                search_query += f" {team}"
            
            return f"""🔍 웹 검색이 필요합니다:

**검색 키워드**: {search_query}

**찾아야 할 정보**:
1. 날짜 및 시간 (한국 시간)
2. 홈팀 vs 원정팀
3. 경기장 정보
4. 중계 방송사 (가능하면)

다음 형식으로 정리해주세요:
📅 [날짜] [시간] KST
   🏟️ [홈팀] vs [원정팀]
   🏆 리그: {league}
"""

        elif name == "get_player_info":
            player_name = args.get("player_name", "")
            include_stats = args.get("include_stats", True)
            
            search_queries = [
                f"{player_name} 선수 프로필 소속팀 포지션",
                f"{player_name} 경력 이적 기록",
                f"{player_name} 2024-25 시즌 통계 골 어시스트" if include_stats else "",
                f"{player_name} 수상 경력 연봉 주급",
            ]
            
            return f"""🔍 웹 검색이 필요합니다:

**검색 키워드**:
{chr(10).join(f'- {q}' for q in search_queries if q)}

**찾아야 할 정보**:
1. 기본 정보
   - 이름 (한글/영문)
   - 국적
   - 생년월일 (나이)
   - 신장/체중

2. 소속 정보
   - 현재 소속팀
   - 포지션
   - 등번호
   - 계약 기간

3. 경력
   - 과거 소속팀 및 기간
   - 이적료 정보

4. 이번 시즌 통계 (2024-25)
   - 출전 경기 수
   - 골 / 어시스트
   - 평점

5. 주요 수상 이력
   - 개인상
   - 팀 우승 기록

6. 시장 가치 및 연봉
   - 이적 시장 가치
   - 연봉 또는 주급 (추정치)

다음 형식으로 정리해주세요:
👤 **{player_name}**
🏴 국적 | 📅 나이 | ⚽ 포지션
🏆 소속: [팀명] (#등번호)
📊 시즌 통계: [골]골 [어시]도움
💰 시장가치: [금액] | 연봉: [금액]
"""

        elif name == "get_league_standings":
            league = args.get("league", "")
            top_n = args.get("top_n", 20)
            
            search_query = f"{league} 순위표 2024-25 시즌 현재"
            
            return f"""🔍 웹 검색이 필요합니다:

**검색 키워드**: {search_query}

**찾아야 할 정보** (상위 {top_n}팀):
1. 순위
2. 팀명
3. 경기수 (승/무/패)
4. 득점 / 실점
5. 득실차
6. 승점

다음 형식으로 정리해주세요:
🏆 **{league} 순위표** (2024-25 시즌)

순위 | 팀명 | 경기 | 승점 | 승 | 무 | 패 | 득실차
-----|------|------|------|----|----|----|---------
1    | [팀] | 10   | 27   | 9  | 0  | 1  | +15
"""

        elif name == "get_league_info":
            league = args.get("league", "")
            
            search_queries = [
                f"{league} 리그 정보 역사",
                f"{league} 참가팀 2024-25 시즌",
                f"{league} 역대 우승팀",
            ]
            
            return f"""🔍 웹 검색이 필요합니다:

**검색 키워드**:
{chr(10).join(f'- {q}' for q in search_queries)}

**찾아야 할 정보**:
1. 리그 기본 정보
   - 공식 명칭
   - 창설 연도
   - 국가
   - 참가팀 수

2. 현재 시즌 정보 (2024-25)
   - 참가팀 목록
   - 시즌 기간
   - 승격/강등 규정

3. 역사
   - 최다 우승팀 (우승 횟수)
   - 최근 3시즌 우승팀
   - 주요 기록

4. 특징
   - 중계권료
   - 리그 레벨 (UEFA 계수)
"""

        elif name == "get_team_info":
            team_name = args.get("team_name", "")
            league = args.get("league", "")
            
            search_query = f"{team_name} 팀 정보 감독 홈구장 2024-25"
            if league:
                search_query += f" {league}"
            
            return f"""🔍 웹 검색이 필요합니다:

**검색 키워드**: {search_query}

**찾아야 할 정보**:
1. 팀 기본 정보
   - 정식 명칭
   - 창단 연도
   - 홈구장 (수용 인원)
   - 연고지

2. 현재 시즌 정보
   - 감독 (부임 시기)
   - 주장
   - 현재 순위
   - 최근 5경기 성적

3. 주요 선수 (스쿼드)
   - 공격수 주전
   - 미드필더 주전
   - 수비수 주전
   - 골키퍼

4. 우승 이력
   - 리그 우승 횟수
   - 컵 대회 우승
"""

        elif name == "get_top_scorers":
            league = args.get("league", "")
            top_n = args.get("top_n", 10)
            
            search_query = f"{league} 득점왕 순위 2024-25 시즌"
            
            return f"""🔍 웹 검색이 필요합니다:

**검색 키워드**: {search_query}

**찾아야 할 정보** (상위 {top_n}명):
1. 순위
2. 선수 이름
3. 소속팀
4. 골 수
5. 어시스트 수 (가능하면)
6. 경기 수

다음 형식으로 정리해주세요:
⚽ **{league} 득점왕 순위** (2024-25 시즌)

순위 | 선수명 | 팀 | 골 | 경기
-----|--------|----|----|------
1    | [이름] | [팀] | 15 | 10
"""

        elif name == "compare_players":
            player1 = args.get("player1", "")
            player2 = args.get("player2", "")
            season = args.get("season", "2024-25")
            
            search_queries = [
                f"{player1} vs {player2} 통계 비교 {season}",
                f"{player1} {season} 시즌 통계",
                f"{player2} {season} 시즌 통계",
            ]
            
            return f"""🔍 웹 검색이 필요합니다:

**검색 키워드**:
{chr(10).join(f'- {q}' for q in search_queries)}

**찾아야 할 정보** ({season} 시즌):
1. 기본 통계
   - 출전 경기 수
   - 골 수
   - 어시스트 수
   - 평점

2. 세부 통계
   - 슈팅 수 / 유효 슈팅
   - 패스 성공률
   - 드리블 성공률
   - 태클 성공 (수비수일 경우)

3. 시장 가치
   - 현재 이적료 추정가

다음 형식으로 비교표 작성:
⚔️ **선수 비교: {player1} vs {player2}**

항목 | {player1} | {player2}
-----|-----------|----------
골   | [수] | [수]
도움 | [수] | [수]
경기 | [수] | [수]
"""

        elif name == "get_transfer_news":
            league = args.get("league", "")
            team = args.get("team", "")
            
            today = datetime.now()
            week_ago = today - timedelta(days=7)
            
            search_query = f"축구 이적 소식 {week_ago.strftime('%Y년 %m월 %d일')} ~ {today.strftime('%Y년 %m월 %d일')}"
            if league:
                search_query += f" {league}"
            if team:
                search_query += f" {team}"
            
            return f"""🔍 웹 검색이 필요합니다:

**검색 키워드**: {search_query}

**찾아야 할 정보**:
1. 확정 이적
   - 선수 이름
   - 이전 팀 → 새 팀
   - 이적료 (알려진 경우)
   - 계약 기간

2. 이적 루머
   - 선수 이름
   - 관심 구단
   - 이적료 추정
   - 신뢰도 (공식 발표/언론 보도)

다음 형식으로 정리:
🔄 **최근 이적 소식**

✅ 확정 이적:
- [선수명]: [구단A] → [구단B] (이적료: [금액], 계약: [기간])

📰 이적 루머:
- [선수명]: [관심구단] 관심 (이적료: [추정], 출처: [언론])
"""

        else:
            return f"❌ 지원하지 않는 도구: {name}"
            
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}"


# FastAPI 엔드포인트
@app.get("/")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "server": "위클리 해축 MCP",
        "version": "1.0.0",
        "supported_leagues": SUPPORTED_LEAGUES,
        "tools_count": len(TOOLS)
    }


@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    """MCP 프로토콜 엔드포인트"""
    
    if request.method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "weekly-soccer-mcp",
                    "version": "1.0.0"
                }
            }
        }
    
    elif request.method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "result": {
                "tools": TOOLS
            }
        }
    
    elif request.method == "tools/call":
        tool_name = request.params.get("name", "")
        arguments = request.params.get("arguments", {})
        
        result = await execute_tool(tool_name, arguments)
        
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": result
                    }
                ]
            }
        }
    
    else:
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {request.method}"
            }
        }


# 서버 실행
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
