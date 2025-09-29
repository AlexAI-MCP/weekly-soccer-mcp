# ⚽ 위클리 해축 MCP - 완성!

## 🎯 프로젝트 요약

**실시간 웹 검색 기반 축구 정보 MCP 서버**

- ✅ **9개 도구** 완전 구현
- ✅ **8개 리그** 지원
- ✅ **로컬 테스트** 성공
- ✅ **Railway 배포** 준비 완료

---

## 📍 프로젝트 위치

```
C:\Users\daewoo111\AppData\Local\AnthropicClaude\app-0.13.37\weekly-soccer-mcp\
```

---

## 🚀 즉시 배포하기

### 방법 1: 원클릭 배포 (가장 빠름)
```bash
cd C:\Users\daewoo111\AppData\Local\AnthropicClaude\app-0.13.37\weekly-soccer-mcp
deploy.bat
```

### 방법 2: 수동 배포
```bash
cd C:\Users\daewoo111\AppData\Local\AnthropicClaude\app-0.13.37\weekly-soccer-mcp
railway login
railway init
railway up
railway domain
```

---

## 📡 PlayMCP 연결

1. Railway 배포 후 생성된 URL 복사
2. PlayMCP에 등록:
   - **Name**: 위클리 해축
   - **URL**: `https://your-app.up.railway.app/mcp`
   - **웹 검색**: ✅ 필수!

3. 테스트:
   ```
   "프리미어리그 지난 주 경기 결과 보여줘"
   "손흥민 선수 정보 알려줘"
   ```

---

## 🛠️ 9개 도구 목록

1. `get_recent_matches` - 지난 7일 경기 결과
2. `get_upcoming_matches` - 다음 7일 경기 일정
3. `get_player_info` - 선수 상세 정보
4. `get_league_standings` - 리그 순위표
5. `get_league_info` - 리그 정보
6. `get_team_info` - 팀 정보
7. `get_top_scorers` - 득점왕 순위
8. `compare_players` - 선수 비교
9. `get_transfer_news` - 이적 소식

---

## 🌍 지원 리그

프리미어리그 | 세리에A | 라리가 | 분데스리가  
K리그1 | J리그 | MLS | 사우디프로리그

---

## 📚 문서

- `README.md` - 프로젝트 개요
- `DEPLOYMENT.md` - 상세 배포 가이드
- `server.py` - 메인 서버 코드 (609줄)

---

## 💡 핵심 특징

- **데이터베이스 불필요**: 실시간 웹 검색만 사용
- **항상 최신 정보**: 검색할 때마다 최신 데이터
- **무료 배포**: Railway 무료 플랜 활용
- **간단한 연동**: PlayMCP 웹 검색 권한만 필요

---

## 🎉 배포 준비 완료!

이제 `deploy.bat`를 실행하여 배포하세요!
