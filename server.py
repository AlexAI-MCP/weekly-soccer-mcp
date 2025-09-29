"""
위클리 해축 (Weekly Soccer) MCP Server v3.0
PlayMCP 웹검색 연동 최적화 - K-Beauty 패턴 적용
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
        "description": """Get recent football match results (last 7 days) by searching the web for the latest scores and fixtures.

This tool provides search queries that should be used to find current match results from official league sources, sports news sites, and football databases.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "League name (e.g., 'Premier League', 'La Liga', 'K League') or 'all'",
                    "default": "all"
                }
            }
        }
    },
    {
        "name": "get_upcoming_matches",
        "description": """Get upcoming football fixtures (next 7 days) by searching the web for scheduled matches and kickoff times.

This tool provides search queries for finding fixture schedules from official league calendars and team websites.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "League name or 'all'",
                    "default": "all"
                }
            }
        }
    },
    {
        "name": "get_player_info",
        "description": """Get comprehensive player information including stats, career history, and current form by searching transfermarkt, official sources, and sports databases.

This tool provides targeted search queries for gathering player statistics and biographical information.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "Player's full name (e.g., 'Son Heung-min')"
                }
            },
            "required": ["player_name"]
        }
    },
    {
        "name": "get_league_standings",
        "description": """Get current league table with points, goals, and positions by searching official league websites and verified sports sources.

This tool provides search queries for accessing the most up-to-date league standings.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "League name (e.g., 'Premier League', 'Bundesliga')"
                }
            },
            "required": ["league"]
        }
    },
    {
        "name": "get_team_info",
        "description": """Get team information, recent form, and squad details by searching official team sites and football news sources.

This tool provides search queries for comprehensive team analysis and current performance.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "Team name (e.g., 'Manchester City', 'Real Madrid')"
                }
            },
            "required": ["team_name"]
        }
    },
    {
        "name": "get_top_scorers",
        "description": """Get leading goalscorers ranking by searching official league statistics and verified football databases.

This tool provides search queries for accessing current top scorer lists with goals and assists.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "League name"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of top scorers",
                    "default": 10
                }
            },
            "required": ["league"]
        }
    }
]

@app.get("/")
async def health():
    return {"status": "healthy", "name": "Weekly Soccer MCP", "version": "3.0"}

@app.post("/mcp")
async def mcp_endpoint(req: MCPRequest):
    if req.method == "initialize":
        return MCPResponse(id=req.id, result={
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "weekly-soccer-mcp", "version": "3.0"}
        })
    
    elif req.method == "tools/list":
        return MCPResponse(id=req.id, result={"tools": TOOLS})
    
    elif req.method == "tools/call":
        tool_name = req.params.get("name")
        arguments = req.params.get("arguments", {})
        try:
            result = await execute_tool(tool_name, arguments)
            return MCPResponse(id=req.id, result={"content": [{"type": "text", "text": result}]})
        except Exception as e:
            return MCPResponse(id=req.id, error={"code": -32603, "message": str(e)})
    
    return MCPResponse(id=req.id, error={"code": -32601, "message": f"Method not found"})

async def execute_tool(name: str, args: Dict) -> str:
    """도구 실행 - 웹검색 가이드 제공"""
    
    if name == "get_recent_matches":
        league = args.get("league", "all")
        if league == "all":
            return """To find recent football match results:

**Recommended web searches:**
1. "football results last 7 days 2025"
2. "축구 경기 결과 이번주"

**What to look for:**
- Official league websites (Premier League, La Liga, etc.)
- ESPN, BBC Sport match results
- Date, teams, scores, competition names

**Expected format:** Date | Home Team vs Away Team | Score | League"""
        
        return f"""To find recent {league} match results:

**Recommended web searches:**
1. "{league} results last week 2025"
2. "{league} 경기 결과 최근"

**Sources to check:**
- Official {league} website
- Major sports news sites
- Verified football databases

**Return format:** Match date, teams, final score, venue"""
    
    elif name == "get_upcoming_matches":
        league = args.get("league", "all")
        if league == "all":
            return """To find upcoming football fixtures:

**Recommended web searches:**
1. "football fixtures next 7 days 2025"
2. "축구 경기 일정 다음주"

**What to look for:**
- Match schedules with dates and times
- Kickoff times in user's timezone
- Venue information

**Expected format:** Date | Time | Home vs Away | Competition"""
        
        return f"""To find upcoming {league} fixtures:

**Recommended web searches:**
1. "{league} fixtures next week 2025"
2. "{league} 경기 일정"

**Sources:** Official {league} calendar, team websites
**Format:** Date, time, matchup, venue"""
    
    elif name == "get_player_info":
        player = args["player_name"]
        return f"""To find information about {player}:

**Recommended web searches:**
1. "{player} player profile stats 2025"
2. "{player} transfermarkt career"
3. "{player} 선수 프로필"

**Key information to gather:**
- Current team and position
- 2024-25 season statistics (goals, assists, appearances)
- Career history and achievements
- Market value and contract details

**Sources:** Transfermarkt, official club sites, verified sports databases"""
    
    elif name == "get_league_standings":
        league = args["league"]
        return f"""To find current {league} standings:

**Recommended web searches:**
1. "{league} table 2024-25 current"
2. "{league} 순위표"

**Essential data:**
- Team positions (1st to last)
- Points, wins, draws, losses
- Goals for, goals against, goal difference
- Recent form (last 5 matches)

**Priority source:** Official {league} website
**Format:** Position | Team | Played | W-D-L | GF-GA | GD | Points"""
    
    elif name == "get_team_info":
        team = args["team_name"]
        return f"""To find information about {team}:

**Recommended web searches:**
1. "{team} team profile 2025"
2. "{team} recent form results"
3. "{team} 팀 정보"

**Key details:**
- Current league position
- Recent match results (last 5 games)
- Top players and manager
- Stadium and club info

**Sources:** Official team website, league sites, sports news"""
    
    elif name == "get_top_scorers":
        league = args["league"]
        limit = args.get("limit", 10)
        return f"""To find top scorers in {league}:

**Recommended web searches:**
1. "{league} top scorers 2024-25"
2. "{league} 득점왕 순위"

**Data needed:**
- Player rankings (top {limit})
- Goals scored this season
- Assists (if available)
- Team information

**Source:** Official {league} statistics page
**Format:** Rank | Player | Team | Goals | Assists"""
    
    return "Tool not found"

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
