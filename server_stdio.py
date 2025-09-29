#!/usr/bin/env python3
"""
위클리 해축 (Weekly Soccer) MCP Server
실시간 웹 검색 기반 축구 정보 제공 (stdio 방식)
"""

import asyncio
import sys
from typing import Any
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import mcp.types as types

# 서버 인스턴스 생성
server = Server("weekly-soccer-mcp")

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

# 리그 이름 정규화 함수
def normalize_league_name(league: str) -> str:
    """리그 이름을 표준화된 형식으로 변환"""
    league_lower = league.lower().strip()
    
    # 프리미어리그
    if any(x in league_lower for x in ["premier", "epl", "프리미어"]):
        return "프리미어리그"
    # 세리에A
    elif any(x in league_lower for x in ["serie", "세리에"]):
        return "세리에A"
    # 라리가
    elif any(x in league_lower for x in ["la liga", "라리가"]):
        return "라리가"
    # 분데스리가
    elif any(x in league_lower for x in ["bundesliga", "분데스"]):
        return "분데스리가"
    # 사우디
    elif any(x in league_lower for x in ["saudi", "사우디"]):
        return "사우디프로리그"
    # K리그
    elif any(x in league_lower for x in ["k league", "k리그", "케이리그"]):
        return "K리그1"
    # J리그
    elif any(x in league_lower for x in ["j league", "j리그", "제이리그"]):
        return "J리그"
    # MLS
    elif "mls" in league_lower:
        return "MLS"
    else:
        return league

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """사용 가능한 도구 목록 반환"""
    return [
        types.Tool(
            name="get_recent_matches",
            description="지난 7일간의 특정 리그 경기 결과를 웹 검색으로 조회합니다. 날짜, 팀명, 스코어, 주요 이벤트를 포함합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "league": {
                        "type": "string",
                        "description": f"리그명 (지원: {', '.join(SUPPORTED_LEAGUES[:8])})"
                    },
                    "team": {
                        "type": "string",
                        "description": "(선택) 특정 팀으로 필터링"
                    }
                },
                "required": ["league"]
            }
        ),
        types.Tool(
            name="get_upcoming_matches",
            description="다음 7일간의 특정 리그 경기 일정을 웹 검색으로 조회합니다. 날짜, 시간, 대진 팀을 포함합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "league": {
                        "type": "string",
                        "description": f"리그명 (지원: {', '.join(SUPPORTED_LEAGUES[:8])})"
                    },
                    "team": {
                        "type": "string",
                        "description": "(선택) 특정 팀으로 필터링"
                    }
                },
                "required": ["league"]
            }
        ),
        types.Tool(
            name="get_player_info",
            description="선수의 상세 정보를 웹 검색으로 조회합니다. 소속팀, 포지션, 통계, 경력, 수상 이력, 연봉 등을 포함합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "player_name": {
                        "type": "string",
                        "description": "선수 이름 (예: 손흥민, Haaland, Mbappe)"
                    }
                },
                "required": ["player_name"]
            }
        ),
        types.Tool(
            name="get_league_standings",
            description="특정 리그의 현재 순위표를 웹 검색으로 조회합니다. 순위, 팀명, 승점, 승/무/패, 득실차를 포함합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "league": {
                        "type": "string",
                        "description": f"리그명 (지원: {', '.join(SUPPORTED_LEAGUES[:8])})"
                    }
                },
                "required": ["league"]
            }
        ),
        types.Tool(
            name="get_league_info",
            description="리그의 역사와 정보를 웹 검색으로 조회합니다. 창설 연도, 참가 팀 수, 역대 우승팀, 특징을 포함합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "league": {
                        "type": "string",
                        "description": f"리그명 (지원: {', '.join(SUPPORTED_LEAGUES[:8])})"
                    }
                },
                "required": ["league"]
            }
        ),
        types.Tool(
            name="get_team_info",
            description="팀의 상세 정보를 웹 검색으로 조회합니다. 감독, 주요 선수, 홈 구장, 최근 성적, 이적 소식을 포함합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "team_name": {
                        "type": "string",
                        "description": "팀 이름 (예: Manchester United, 토트넘, 인터밀란)"
                    },
                    "league": {
                        "type": "string",
                        "description": "(선택) 소속 리그 (동명 팀 구분용)"
                    }
                },
                "required": ["team_name"]
            }
        ),
        types.Tool(
            name="get_top_scorers",
            description="특정 리그의 득점왕 순위를 웹 검색으로 조회합니다. 선수명, 소속팀, 골 수를 포함합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "league": {
                        "type": "string",
                        "description": f"리그명 (지원: {', '.join(SUPPORTED_LEAGUES[:8])})"
                    },
                    "limit": {
                        "type": "number",
                        "description": "조회할 순위 수 (기본: 10)",
                        "default": 10
                    }
                },
                "required": ["league"]
            }
        ),
        types.Tool(
            name="compare_players",
            description="두 선수의 통계를 비교합니다. 골, 어시스트, 평점 등을 웹 검색으로 조회하여 비교합니다.",
            inputSchema={
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
                        "description": "(선택) 시즌 (기본: 현재 시즌)",
                        "default": "2024-25"
                    }
                },
                "required": ["player1", "player2"]
            }
        ),
        types.Tool(
            name="get_transfer_news",
            description="최근 이적 소식을 웹 검색으로 조회합니다. 확정 이적, 이적 루머, 이적료 정보를 포함합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "league": {
                        "type": "string",
                        "description": f"(선택) 특정 리그로 필터링 (지원: {', '.join(SUPPORTED_LEAGUES[:8])})"
                    },
                    "team": {
                        "type": "string",
                        "description": "(선택) 특정 팀으로 필터링"
                    },
                    "player": {
                        "type": "string",
                        "description": "(선택) 특정 선수로 필터링"
                    }
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """도구 호출 처리"""
    
    if not arguments:
        arguments = {}
    
    try:
        if name == "get_recent_matches":
            league = normalize_league_name(arguments.get("league", ""))
            team = arguments.get("team")
            
            team_filter = f"\n**특정 팀**: {team}" if team else ""
            
            search_request = f"""🔍 **웹 검색 요청: {league} 최근 경기 결과**
{team_filter}

다음 정보를 웹에서 검색해 주세요:
1. **지난 7일간 {league} 경기 결과**
2. **날짜별 경기 일정**
3. **각 경기의 스코어** (예: 맨체스터 유나이티드 3-1 첼시)
4. **득점자 및 주요 이벤트** (골, 어시스트, 경고/퇴장)

**검색 키워드**: `{league} 경기 결과 최근 7일 2024-25 시즌`
"""
            return [types.TextContent(type="text", text=search_request)]
        
        elif name == "get_upcoming_matches":
            league = normalize_league_name(arguments.get("league", ""))
            team = arguments.get("team")
            
            team_filter = f"\n**특정 팀**: {team}" if team else ""
            
            search_request = f"""🔍 **웹 검색 요청: {league} 다가오는 경기 일정**
{team_filter}

다음 정보를 웹에서 검색해 주세요:
1. **다음 7일간 {league} 경기 일정**
2. **날짜 및 시간** (한국 시간 기준)
3. **대진 카드** (홈팀 vs 원정팀)
4. **경기 장소** (스타디움)

**검색 키워드**: `{league} 경기 일정 다음 주 2024-25 시즌`
"""
            return [types.TextContent(type="text", text=search_request)]
        
        elif name == "get_player_info":
            player_name = arguments.get("player_name", "")
            
            search_request = f"""🔍 **웹 검색 요청: {player_name} 선수 정보**

다음 정보를 웹에서 검색해 주세요:
1. **기본 정보**
   - 소속팀, 포지션, 등번호
   - 생년월일, 국적, 신체 정보

2. **경력**
   - 이전 소속 팀 및 이적 기록
   - 주요 경력 사항

3. **2024-25 시즌 통계**
   - 출전 경기 수
   - 골 / 어시스트
   - 평점 및 주요 기록

4. **수상 이력**
   - 개인 수상 (득점왕, MVP 등)
   - 팀 우승 기록

5. **시장 가치 & 연봉**
   - 현재 이적 시장 가치
   - 추정 연봉 / 주급

**검색 키워드**: `{player_name} 선수 프로필 소속팀 포지션 통계 경력 연봉 2024`
"""
            return [types.TextContent(type="text", text=search_request)]
        
        elif name == "get_league_standings":
            league = normalize_league_name(arguments.get("league", ""))
            
            search_request = f"""🔍 **웹 검색 요청: {league} 현재 순위표**

다음 정보를 웹에서 검색해 주세요:
1. **순위** (1위~20위)
2. **팀명**
3. **경기 수** (총 경기)
4. **승점**
5. **승 / 무 / 패**
6. **득실차** (득점 - 실점)
7. **최근 5경기 폼** (W/D/L)

**검색 키워드**: `{league} 순위표 2024-25 시즌 현재`
"""
            return [types.TextContent(type="text", text=search_request)]
        
        elif name == "get_league_info":
            league = normalize_league_name(arguments.get("league", ""))
            
            search_request = f"""🔍 **웹 검색 요청: {league} 리그 정보**

다음 정보를 웹에서 검색해 주세요:
1. **리그 개요**
   - 공식 명칭 및 약칭
   - 창설 연도
   - 주관 기구

2. **리그 구조**
   - 참가 팀 수
   - 리그 시스템 (승강제 등)
   - 시즌 기간

3. **역대 우승팀**
   - 최다 우승팀
   - 최근 5시즌 우승팀

4. **주요 특징**
   - 리그 특성
   - 유명 클럽
   - 글로벌 인기도

**검색 키워드**: `{league} 리그 정보 역사 우승팀 특징`
"""
            return [types.TextContent(type="text", text=search_request)]
        
        elif name == "get_team_info":
            team_name = arguments.get("team_name", "")
            league = arguments.get("league")
            
            league_filter = f"\n**소속 리그**: {normalize_league_name(league)}" if league else ""
            
            search_request = f"""🔍 **웹 검색 요청: {team_name} 팀 정보**
{league_filter}

다음 정보를 웹에서 검색해 주세요:
1. **팀 기본 정보**
   - 정식 명칭
   - 창단 연도
   - 홈 구장
   - 감독

2. **주요 선수**
   - 핵심 선수 리스트 (공격수, 미드필더, 수비수, 골키퍼)
   - 주장

3. **최근 성적**
   - 2024-25 시즌 현재 순위
   - 최근 5경기 결과
   - 주요 대회 진출 현황

4. **이적 소식**
   - 최근 영입 선수
   - 이적 루머

**검색 키워드**: `{team_name} 팀 정보 감독 주요선수 최근 성적 2024`
"""
            return [types.TextContent(type="text", text=search_request)]
        
        elif name == "get_top_scorers":
            league = normalize_league_name(arguments.get("league", ""))
            limit = arguments.get("limit", 10)
            
            search_request = f"""🔍 **웹 검색 요청: {league} 득점왕 순위**

다음 정보를 웹에서 검색해 주세요:
1. **순위** (상위 {limit}명)
2. **선수 이름**
3. **소속 팀**
4. **골 수**
5. **출전 경기 수**
6. **경기당 평균 골**

**검색 키워드**: `{league} 득점왕 순위 2024-25 시즌 골 득점자`
"""
            return [types.TextContent(type="text", text=search_request)]
        
        elif name == "compare_players":
            player1 = arguments.get("player1", "")
            player2 = arguments.get("player2", "")
            season = arguments.get("season", "2024-25")
            
            search_request = f"""🔍 **웹 검색 요청: {player1} vs {player2} 통계 비교**

**시즌**: {season}

다음 정보를 웹에서 검색해 주세요:

**{player1}**
- 소속팀, 포지션
- 출전 경기 수
- 골 / 어시스트
- 평점
- 시장 가치

**{player2}**
- 소속팀, 포지션
- 출전 경기 수
- 골 / 어시스트
- 평점
- 시장 가치

**비교 분석**:
- 득점 효율성
- 어시스트 기여도
- 전반적인 활약도

**검색 키워드**: `{player1} vs {player2} 통계 비교 {season} 시즌`
"""
            return [types.TextContent(type="text", text=search_request)]
        
        elif name == "get_transfer_news":
            league = arguments.get("league")
            team = arguments.get("team")
            player = arguments.get("player")
            
            filters = []
            if league:
                filters.append(f"**리그**: {normalize_league_name(league)}")
            if team:
                filters.append(f"**팀**: {team}")
            if player:
                filters.append(f"**선수**: {player}")
            
            filter_text = "\n".join(filters) if filters else "**전체 리그**"
            
            search_keywords = " ".join(filter(None, [
                league if league else "",
                team if team else "",
                player if player else "",
                "이적 소식"
            ]))
            
            search_request = f"""🔍 **웹 검색 요청: 최근 이적 소식**

{filter_text}

다음 정보를 웹에서 검색해 주세요:
1. **확정 이적**
   - 선수 이름
   - 이적 출발지 → 도착지
   - 이적료 (또는 자유 이적)
   - 계약 기간

2. **이적 루머 & 협상 중**
   - 관심 선수 및 팀
   - 이적 가능성
   - 예상 이적료

3. **임대 이적**
   - 임대 출발지 → 도착지
   - 임대 기간

**검색 키워드**: `{search_keywords} 2024 최근`
"""
            return [types.TextContent(type="text", text=search_request)]
        
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ 알 수 없는 도구: {name}"
            )]
    
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ 오류 발생: {str(e)}"
        )]

async def main():
    """메인 실행 함수"""
    # stdio 서버 실행
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weekly-soccer-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
