"""
위클리 해축 (Weekly Soccer) MCP Server v2.1
실시간 웹 검색 기반 축구 정보 제공 (Direct Web Search Trigger)
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
This tool will return a web search query that Claude MUST execute.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {"type": "string", "description": "League name", "default": "all"}
            }
        }
    },
    {
        "name": "get_upcoming_matches",
        "description": """Get upcoming fixtures for the next 7 days.
This tool will return a web search query that Claude MUST execute.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {"type": "string", "description": "League name", "default": "all"}
            }
        }
    },
    {
        "name": "get_player_info",
        "description": """Get detailed player information.
This tool will return a web search query that Claude MUST execute.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "player_name": {"type": "string", "description": "Player's full name"}
            },
            "required": ["player_name"]
        }
    },
    {
        "name": "get_league_standings",
        "description": """Get current league standings.
This tool will return a web search query that Claude MUST execute.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {"type": "string", "description": "League name"}
            },
            "required": ["league"]
        }
    },
    {
        "name": "get_team_info",
        "description": """Get team information and recent form.
This tool will return a web search query that Claude MUST execute.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "team_name": {"type": "string", "description": "Team name"}
            },
            "required": ["team_name"]
        }
    },
    {
        "name": "get_top_scorers",
        "description": """Get top scorers list.
This tool will return a web search query that Claude MUST execute.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {"type": "string", "description": "League name"},
                "limit": {"type": "integer", "description": "Number of players", "default": 10}
            },
            "required": ["league"]
        }
    }
]

@app.get("/")
async def health():
    return {"status": "healthy", "name": "Weekly Soccer MCP", "version": "2.1"}

@app.post("/mcp")
async def mcp_endpoint(req: MCPRequest):
    if req.method == "initialize":
        return MCPResponse(id=req.id, result={
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "weekly-soccer-mcp", "version": "2.1"}
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
    if name == "get_recent_matches":
        league = args.get("league", "all")
        if league == "all":
            return "Search: '축구 경기 결과 최근 7일' OR 'football match results last 7 days'"
        return f"Search: '{league} 경기 결과 최근 7일' OR '{league} match results last week 2025'"
    
    elif name == "get_upcoming_matches":
        league = args.get("league", "all")
        if league == "all":
            return "Search: '축구 경기 일정 다음 7일' OR 'football fixtures next 7 days'"
        return f"Search: '{league} 경기 일정 다음 7일' OR '{league} upcoming fixtures next week 2025'"
    
    elif name == "get_player_info":
        player = args["player_name"]
        return f"Search: '{player} 선수 프로필 통계' OR '{player} player stats transfermarkt 2025'"
    
    elif name == "get_league_standings":
        league = args["league"]
        return f"Search: '{league} 순위표' OR '{league} table standings 2025'"
    
    elif name == "get_team_info":
        team = args["team_name"]
        return f"Search: '{team} 팀 정보' OR '{team} team recent results 2025'"
    
    elif name == "get_top_scorers":
        league = args["league"]
        limit = args.get("limit", 10)
        return f"Search: '{league} 득점왕' OR '{league} top scorers 2024-25 (top {limit})'"
    
    return "Tool not found"

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
