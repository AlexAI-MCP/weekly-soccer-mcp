"""
위클리 해축 (Weekly Soccer) MCP Server v2.0
실시간 웹 검색 기반 축구 정보 제공 (PlayMCP 웹검색 자동 트리거 최적화)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, Optional
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Any
    method: str
    params: Dict[str, Any] = {}

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Any
    result: Any = None
    error: Optional[Dict[str, Any]] = None

TOOLS = [
    {
        "name": "get_recent_matches",
        "description": """Get football match results from the last 7 days.
        
⚠️ IMPORTANT: This tool REQUIRES current web data.
After calling this tool, you MUST search the web for the latest match results.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "League name (e.g., 'Premier League', 'La Liga', 'K League') or 'all' for all leagues",
                    "default": "all"
                }
            }
        }
    },
    {
        "name": "get_upcoming_matches",
        "description": """Get upcoming football match fixtures for the next 7 days.
        
⚠️ IMPORTANT: This tool REQUIRES current web data.
After calling this tool, you MUST search the web for the latest fixtures.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "League name or 'all' for all leagues",
                    "default": "all"
                }
            }
        }
    },
    {
        "name": "get_player_info",
        "description": """Get detailed information about a football player.
        
⚠️ IMPORTANT: This tool REQUIRES current web data.
After calling this tool, you MUST search the web for player stats and information.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "Player's full name (e.g., 'Son Heung-min', 'Erling Haaland')"
                }
            },
            "required": ["player_name"]
        }
    },
    {
        "name": "get_league_standings",
        "description": """Get current league standings/table.
        
⚠️ IMPORTANT: This tool REQUIRES current web data.
After calling this tool, you MUST search the web for the latest league table.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "League name: Premier League, La Liga, Serie A, Bundesliga, Ligue 1, Saudi Pro League, K League, J League, MLS"
                }
            },
            "required": ["league"]
        }
    },
    {
        "name": "get_team_info",
        "description": """Get detailed information about a football team.
        
⚠️ IMPORTANT: This tool REQUIRES current web data.
After calling this tool, you MUST search the web for team information and recent form.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "Team name (e.g., 'Manchester City', 'Real Madrid', 'Bayern Munich')"
                }
            },
            "required": ["team_name"]
        }
    },
    {
        "name": "get_top_scorers",
        "description": """Get top scorers list for a specific league.
        
⚠️ IMPORTANT: This tool REQUIRES current web data.
After calling this tool, you MUST search the web for the latest top scorers list.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "League name (e.g., 'Premier League', 'Champions League')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of top scorers to return",
                    "default": 10
                }
            },
            "required": ["league"]
        }
    }
]

@app.get("/")
async def health():
    return {
        "status": "healthy",
        "name": "Weekly Soccer MCP",
        "version": "2.0",
        "tools": len(TOOLS),
        "requires_web_search": True
    }

@app.post("/mcp")
async def mcp_endpoint(req: MCPRequest):
    if req.method == "initialize":
        return MCPResponse(
            id=req.id,
            result={
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "weekly-soccer-mcp",
                    "version": "2.0"
                }
            }
        )
    
    elif req.method == "tools/list":
        return MCPResponse(
            id=req.id,
            result={"tools": TOOLS}
        )
    
    elif req.method == "tools/call":
        tool_name = req.params.get("name")
        arguments = req.params.get("arguments", {})
        
        try:
            result = await execute_tool(tool_name, arguments)
            return MCPResponse(
                id=req.id,
                result={
                    "content": [
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                }
            )
        except Exception as e:
            return MCPResponse(
                id=req.id,
                error={
                    "code": -32603,
                    "message": str(e)
                }
            )
    
    return MCPResponse(
        id=req.id,
        error={
            "code": -32601,
            "message": f"Method not found: {req.method}"
        }
    )

async def execute_tool(name: str, args: Dict) -> str:
    """도구 실행 - 웹검색 요청 메시지 반환"""
    
    if name == "get_recent_matches":
        league = args.get("league", "all")
        query = f"{league} 경기 결과 최근 7일" if league != "all" else "축구 경기 결과 최근 7일"
        alt_query = f"{league} match results last 7 days 2025"
        
        return f"""🔍 **최근 7일 경기 결과 검색 필요**

TO GET THIS INFORMATION, please search the web now:

**Query 1:** "{query}"
**Query 2:** "{alt_query}"

Look for: Official league sites, ESPN, BBC Sport
Return: Date, Home Team, Score, Away Team, Competition
"""
    
    elif name == "get_upcoming_matches":
        league = args.get("league", "all")
        query = f"{league} 경기 일정 다음 7일" if league != "all" else "축구 경기 일정 다음 7일"
        alt_query = f"{league} upcoming fixtures next 7 days 2025"
        
        return f"""🔍 **다음 7일 경기 일정 검색 필요**

TO GET THIS INFORMATION, please search the web now:

**Query 1:** "{query}"
**Query 2:** "{alt_query}"

Look for: Official league calendars, team websites
Return: Date, Time, Home vs Away, Competition
"""
    
    elif name == "get_player_info":
        player = args["player_name"]
        query = f"{player} 선수 프로필 통계 2024-25"
        alt_query = f"{player} transfermarkt profile stats career"
        
        return f"""🔍 **선수 정보 검색 필요: {player}**

TO GET THIS INFORMATION, please search the web now:

**Query 1:** "{query}"
**Query 2:** "{alt_query}"

Look for: Transfermarkt, official club sites, sports news
Return: Position, Current Team, Stats (Goals/Assists), Career, Awards, Salary
"""
    
    elif name == "get_league_standings":
        league = args["league"]
        query = f"{league} 순위표 2024-25 시즌"
        alt_query = f"{league} table standings current 2025"
        
        return f"""🔍 **리그 순위표 검색 필요: {league}**

TO GET THIS INFORMATION, please search the web now:

**Query 1:** "{query}"
**Query 2:** "{alt_query}"

Look for: Official league website (priority), ESPN, BBC Sport
Return: Position, Team, Played, Won, Drawn, Lost, GF, GA, GD, Points
"""
    
    elif name == "get_team_info":
        team = args["team_name"]
        query = f"{team} 팀 정보 최근 경기 순위 2025"
        alt_query = f"{team} current form recent results 2025"
        
        return f"""🔍 **팀 정보 검색 필요: {team}**

TO GET THIS INFORMATION, please search the web now:

**Query 1:** "{query}"
**Query 2:** "{alt_query}"

Look for: Official team website, league position, recent form
Return: Current Position, Recent Results (W/D/L), Key Players, Manager, Stadium
"""
    
    elif name == "get_top_scorers":
        league = args["league"]
        limit = args.get("limit", 10)
        query = f"{league} 득점왕 순위 2024-25"
        alt_query = f"{league} top scorers 2024-25 season"
        
        return f"""🔍 **득점왕 순위 검색 필요: {league}**

TO GET THIS INFORMATION, please search the web now:

**Query 1:** "{query}"
**Query 2:** "{alt_query}"

Look for: Official league statistics
Return: Rank, Player, Team, Goals, Assists (top {limit} players)
"""
    
    return "Tool not found"

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
