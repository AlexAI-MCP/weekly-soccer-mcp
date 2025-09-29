# 위클리 해축 MCP 서버

실시간 웹 검색 기반 축구 정보 제공 MCP 서버

## 🎯 주요 기능

### 📅 경기 정보
- **지난 7일 경기 결과**: 날짜별 스코어, 득점자
- **다음 7일 경기 일정**: 시간, 대진 카드

### ⚽ 선수 정보
- 소속팀, 포지션, 경력
- 시즌 통계 (골/어시스트)
- 수상 이력, 연봉 정보

### 🏆 리그 정보
- 현재 순위표
- 리그 역사 및 우승 기록
- 득점왕 순위

### 🔄 추가 기능
- 팀 정보 조회
- 선수 비교
- 이적 소식

## 🌍 지원 리그

- 프리미어리그 (EPL)
- 세리에A
- 라리가
- 분데스리가
- 사우디프로리그
- K리그1
- J리그
- MLS

## 🚀 배포 방법

### Railway 배포
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
railway init

# 배포
railway up

# 도메인 생성
railway domain
```

### 로컬 테스트
```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python server.py

# 테스트
curl http://localhost:8080/
```

## 📡 MCP 엔드포인트

배포 후 다음 URL을 PlayMCP에 등록:
```
https://your-app.up.railway.app/mcp
```

## ⚙️ PlayMCP 설정

1. **Server URL**: `https://your-app.up.railway.app/mcp`
2. **웹 검색 권한**: ✅ 활성화 필수
3. **이미지 분석**: ❌ 불필요

## 🔧 도구 목록

1. `get_recent_matches` - 지난 7일 경기 결과
2. `get_upcoming_matches` - 다음 7일 경기 일정
3. `get_player_info` - 선수 상세 정보
4. `get_league_standings` - 리그 순위표
5. `get_league_info` - 리그 정보
6. `get_team_info` - 팀 정보
7. `get_top_scorers` - 득점왕 순위
8. `compare_players` - 선수 비교
9. `get_transfer_news` - 이적 소식

## 📝 사용 예시

### PlayMCP에서 테스트
```
"프리미어리그 지난 주 경기 결과 보여줘"
"손흥민 선수 정보 알려줘"
"세리에A 현재 순위는?"
"음바페와 홀란드 비교해줘"
```

## 🛠️ 기술 스택

- FastAPI
- Python 3.11+
- Railway (배포)

## 📄 라이선스

MIT
