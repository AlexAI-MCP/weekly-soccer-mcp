# ⚽ Weekly Soccer MCP v4.0

**Real-time football data powered by Football-Data.org API**

## 🎯 Features

### 📊 Live Data
- ✅ Real match results (last 7 days)
- ✅ Upcoming fixtures (next 7 days)  
- ✅ Live league standings
- ✅ Team information
- ✅ Team search across leagues

### 🏆 Supported Leagues
- Premier League (England)
- La Liga (Spain)
- Bundesliga (Germany)
- Serie A (Italy)
- Ligue 1 (France)
- Champions League
- Europa League

## 🚀 Quick Start

### 1. Get API Key
Sign up at [Football-Data.org](https://www.football-data.org/client/register) (Free tier: 10 req/min)

### 2. Deploy to Railway

```bash
# Clone repository
git clone https://github.com/AlexAI-MCP/weekly-soccer-mcp.git
cd weekly-soccer-mcp

# Set environment variable in Railway dashboard
FOOTBALL_API_KEY=your_api_key_here

# Railway will auto-deploy
railway up
```

### 3. Register on PlayMCP

```
URL: https://your-app.up.railway.app/mcp
Name: Weekly Soccer MCP
Description: Real-time football data
```

## 🎮 Usage Examples

```
"프리미어리그 최근 경기 결과 알려줘"
→ Shows last 10 matches with scores

"라리가 다음주 경기 일정은?"
→ Shows upcoming fixtures for next 7 days

"세리에A 현재 순위표 보여줘"
→ Displays live standings table

"맨체스터 유나이티드 정보 알려줘"
→ Team details, stadium, founded year

"토트넘 검색"
→ Finds team across all leagues
```

## 🛠️ Tools

| Tool | Description |
|------|-------------|
| `get_recent_matches` | Match results (last 7 days) |
| `get_upcoming_matches` | Fixtures (next 7 days) |
| `get_league_standings` | Current standings table |
| `get_team_info` | Team details |
| `search_team` | Search teams by name |

## 📈 API Details

- **Provider:** Football-Data.org
- **Update Frequency:** Near real-time (1-2 min delay)
- **Free Tier:** 10 requests/minute
- **Rate Limit:** Sufficient for most use cases

## 🔧 Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export FOOTBALL_API_KEY=your_key

# Run locally
python server.py

# Test endpoint
curl http://localhost:8080
```

## 📝 Changelog

### v4.0.0 (2025-09-29)
- ✅ Football-Data.org API integration
- ✅ Real-time match data
- ✅ Live standings updates
- ✅ Team search functionality
- ✅ Removed web search dependency

### v3.0.0 (2025-09-29)
- Attempted web search integration (deprecated)

### v2.0.0 (2025-09-29)
- Optimized for PlayMCP (deprecated)

### v1.0.0 (2025-09-29)
- Initial release (web search only)

## 🎯 Roadmap

- [ ] Player statistics
- [ ] Live match commentary
- [ ] Match predictions
- [ ] Historical data analysis
- [ ] More leagues (MLS, J-League, K-League via alternative APIs)

## 📄 License

MIT

## 🙏 Credits

- Data: [Football-Data.org](https://www.football-data.org/)
- Framework: [FastAPI](https://fastapi.tiangolo.com/)
- Platform: [Railway](https://railway.app/)

---

Made with ⚽ for PlayMCP
