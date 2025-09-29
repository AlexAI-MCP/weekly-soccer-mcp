"""
Weekly Soccer MCP v4.0 - Football-Data.org API Integration
Real-time football data with actual API calls
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict, Optional
import httpx
import os
from datetime import datetime, timedelta

app = FastAPI(title="Weekly Soccer MCP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Football-Data.org API Configuration
API_KEY = os.environ.get("FOOTBALL_API_KEY", "8acc268e54594f698d695ab84a9adc38")
API_BASE = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# League mappings
LEAGUE_CODES = {
    "Premier League": "PL",
    "La Liga": "PD",
    "Bundesliga": "BL1",
    "Serie A": "SA",
    "Ligue 1": "FL1",
    "Champions League": "CL",
    "Europa League": "EL",
}


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Any
    method: str
    params: Dict[str, Any] = {}


# Tool definitions
TOOLS = [
    {
        "name": "get_recent_matches",
        "description": """Get recent football match results from the last 7 days.
        
        Supports: Premier League, La Liga, Bundesliga, Serie A, Ligue 1, Champions League, Europa League.
        Returns actual match data with scores, dates, and teams.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "League name (e.g., 'Premier League', 'La Liga')",
                }
            },
            "required": ["league"],
        },
    },
    {
        "name": "get_upcoming_matches",
        "description": """Get upcoming football matches for the next 7 days.
        
        Supports major European leagues and competitions.
        Returns scheduled fixtures with dates and times.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "League name",
                }
            },
            "required": ["league"],
        },
    },
    {
        "name": "get_league_standings",
        "description": """Get current league standings/table.
        
        Returns live standings with: Position, Team, Played, Won, Drawn, Lost, Points, Goal Difference.
        Updated after every match.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "league": {
                    "type": "string",
                    "description": "League name",
                }
            },
            "required": ["league"],
        },
    },
    {
        "name": "get_team_info",
        "description": """Get detailed information about a specific team.
        
        Returns: Full name, founded year, stadium, colors, website, squad size.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "team_name": {
                    "type": "string",
                    "description": "Team name to search for",
                }
            },
            "required": ["team_name"],
        },
    },
    {
        "name": "search_team",
        "description": """Search for teams by name across all leagues.
        
        Useful when you don't know the exact team name.""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Team name or partial name",
                }
            },
            "required": ["query"],
        },
    },
]


async def fetch_api(endpoint: str) -> Dict:
    """Fetch data from Football-Data.org API"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{API_BASE}{endpoint}", headers=HEADERS)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        return {"error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def format_match(match: Dict) -> str:
    """Format a single match for display"""
    home = match.get("homeTeam", {}).get("name", "Unknown")
    away = match.get("awayTeam", {}).get("name", "Unknown")
    home_score = match.get("score", {}).get("fullTime", {}).get("home")
    away_score = match.get("score", {}).get("fullTime", {}).get("away")
    status = match.get("status", "SCHEDULED")
    utc_date = match.get("utcDate", "")
    
    # Parse date
    try:
        dt = datetime.fromisoformat(utc_date.replace("Z", "+00:00"))
        date_str = dt.strftime("%Y-%m-%d %H:%M")
    except:
        date_str = utc_date
    
    if status == "FINISHED" and home_score is not None and away_score is not None:
        return f"{date_str} | {home} {home_score} - {away_score} {away} [FT]"
    elif status == "IN_PLAY":
        return f"{date_str} | {home} vs {away} [LIVE]"
    else:
        return f"{date_str} | {home} vs {away}"


def format_standings(standings_data: Dict) -> str:
    """Format league standings table"""
    if "error" in standings_data:
        return standings_data["error"]
    
    standings = standings_data.get("standings", [])
    if not standings:
        return "No standings data available"
    
    # Get the main table (usually first one)
    table = standings[0].get("table", [])
    
    lines = ["📊 League Standings\n"]
    lines.append("Pos | Team | P | W | D | L | GD | Pts")
    lines.append("-" * 50)
    
    for entry in table:
        pos = entry.get("position", "-")
        team = entry.get("team", {}).get("name", "Unknown")
        played = entry.get("playedGames", 0)
        won = entry.get("won", 0)
        draw = entry.get("draw", 0)
        lost = entry.get("lost", 0)
        gd = entry.get("goalDifference", 0)
        points = entry.get("points", 0)
        
        lines.append(f"{pos:2} | {team[:20]:20} | {played:2} | {won:2} | {draw:2} | {lost:2} | {gd:+3} | {points:2}")
    
    return "\n".join(lines)


async def execute_tool(name: str, args: Dict) -> str:
    """Execute tool logic with actual API calls"""
    
    if name == "get_recent_matches":
        league = args.get("league", "")
        league_code = LEAGUE_CODES.get(league)
        
        if not league_code:
            return f"❌ League '{league}' not supported. Available: {', '.join(LEAGUE_CODES.keys())}"
        
        # Get matches from last 7 days
        date_from = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
        date_to = datetime.utcnow().strftime("%Y-%m-%d")
        
        data = await fetch_api(f"/competitions/{league_code}/matches?dateFrom={date_from}&dateTo={date_to}")
        
        if "error" in data:
            return f"❌ {data['error']}"
        
        matches = data.get("matches", [])
        if not matches:
            return f"No matches found for {league} in the last 7 days"
        
        # Filter finished matches
        finished = [m for m in matches if m.get("status") == "FINISHED"]
        
        if not finished:
            return f"No finished matches for {league} in the last 7 days"
        
        lines = [f"⚽ Recent {league} Results (Last 7 Days)\n"]
        for match in finished[-10:]:  # Last 10 matches
            lines.append(format_match(match))
        
        return "\n".join(lines)
    
    elif name == "get_upcoming_matches":
        league = args.get("league", "")
        league_code = LEAGUE_CODES.get(league)
        
        if not league_code:
            return f"❌ League '{league}' not supported"
        
        # Get matches for next 7 days
        date_from = datetime.utcnow().strftime("%Y-%m-%d")
        date_to = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")
        
        data = await fetch_api(f"/competitions/{league_code}/matches?dateFrom={date_from}&dateTo={date_to}")
        
        if "error" in data:
            return f"❌ {data['error']}"
        
        matches = data.get("matches", [])
        if not matches:
            return f"No upcoming matches for {league} in the next 7 days"
        
        lines = [f"📅 Upcoming {league} Fixtures (Next 7 Days)\n"]
        for match in matches[:15]:  # Next 15 matches
            lines.append(format_match(match))
        
        return "\n".join(lines)
    
    elif name == "get_league_standings":
        league = args.get("league", "")
        league_code = LEAGUE_CODES.get(league)
        
        if not league_code:
            return f"❌ League '{league}' not supported"
        
        data = await fetch_api(f"/competitions/{league_code}/standings")
        return format_standings(data)
    
    elif name == "get_team_info":
        team_name = args.get("team_name", "")
        
        # Search across all competitions
        all_teams = []
        for league_code in ["PL", "PD", "BL1", "SA", "FL1"]:
            data = await fetch_api(f"/competitions/{league_code}/teams")
            if "teams" in data:
                all_teams.extend(data["teams"])
        
        # Find matching team
        team = None
        team_name_lower = team_name.lower()
        for t in all_teams:
            if team_name_lower in t.get("name", "").lower() or team_name_lower in t.get("shortName", "").lower():
                team = t
                break
        
        if not team:
            return f"❌ Team '{team_name}' not found"
        
        lines = [
            f"⚽ {team.get('name', 'Unknown')}",
            f"Short Name: {team.get('shortName', '-')}",
            f"Founded: {team.get('founded', '-')}",
            f"Stadium: {team.get('venue', '-')}",
            f"Website: {team.get('website', '-')}",
            f"Colors: {team.get('clubColors', '-')}",
        ]
        
        return "\n".join(lines)
    
    elif name == "search_team":
        query = args.get("query", "").lower()
        
        # Search across all competitions
        all_teams = []
        for league_code in ["PL", "PD", "BL1", "SA", "FL1"]:
            data = await fetch_api(f"/competitions/{league_code}/teams")
            if "teams" in data:
                all_teams.extend(data["teams"])
        
        # Find matching teams
        matches = [t for t in all_teams if query in t.get("name", "").lower() or query in t.get("shortName", "").lower()]
        
        if not matches:
            return f"No teams found matching '{query}'"
        
        lines = ["🔍 Search Results:\n"]
        for team in matches[:10]:  # Top 10 results
            lines.append(f"- {team.get('name', 'Unknown')} ({team.get('shortName', '-')})")
        
        return "\n".join(lines)
    
    return f"Unknown tool: {name}"


@app.get("/")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Weekly Soccer MCP v4.0",
        "api": "Football-Data.org",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/mcp")
async def mcp_endpoint(req: MCPRequest):
    """Main MCP endpoint"""
    try:
        if req.method == "initialize":
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": req.id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "weekly-soccer-mcp",
                        "version": "4.0.0"
                    },
                },
            })
        
        elif req.method == "tools/list":
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": req.id,
                "result": {"tools": TOOLS},
            })
        
        elif req.method == "tools/call":
            tool_name = req.params.get("name")
            tool_args = req.params.get("arguments", {})
            
            result_text = await execute_tool(tool_name, tool_args)
            
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": req.id,
                "result": {
                    "content": [{"type": "text", "text": result_text}],
                    "isError": False,
                },
            })
        
        else:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": req.id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {req.method}",
                },
            })
    
    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req.id if hasattr(req, "id") else None,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
        })


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
