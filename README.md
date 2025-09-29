# 위클리 해축 (Weekly Soccer) MCP

⚽ 실시간 웹 검색 기반 전 세계 축구 정보 제공 MCP 서버

## 🎯 주요 기능

### 📅 경기 정보
- **최근 경기 결과**: 지난 7일간의 경기 결과 및 스코어
- **다가오는 경기**: 다음 7일간의 경기 일정

### 👤 선수 정보
- 소속팀, 포지션, 통계
- 경력 및 수상 이력
- 연봉 및 시장 가치

### 🏆 리그 정보
- 실시간 순위표
- 리그 역사 및 특징
- 득점왕 순위

### ⚡ 추가 기능
- 팀 상세 정보
- 선수 통계 비교
- 이적 소식

## 🌍 지원 리그 (8개)

- ⚽ **프리미어리그** (EPL)
- ⚽ **세리에A** (Serie A)
- ⚽ **라리가** (La Liga)
- ⚽ **분데스리가** (Bundesliga)
- ⚽ **사우디프로리그** (Saudi Pro League)
- ⚽ **K리그1** (K League 1)
- ⚽ **J리그** (J League)
- ⚽ **MLS** (Major League Soccer)

## 🛠️ 제공 도구 (9개)

1. `get_recent_matches` - 지난 7일 경기 결과
2. `get_upcoming_matches` - 다음 7일 경기 일정
3. `get_player_info` - 선수 상세 정보
4. `get_league_standings` - 리그 순위표
5. `get_league_info` - 리그 역사/정보
6. `get_team_info` - 팀 상세 정보
7. `get_top_scorers` - 득점왕 순위
8. `compare_players` - 선수 통계 비교
9. `get_transfer_news` - 이적 소식

## 🚀 PlayMCP 등록 방법

### 📡 stdio 방식 (권장)

이 MCP는 stdio 방식으로 작동합니다.

#### 등록 정보

```
서버명: 위클리 해축
설명: 실시간 웹 검색 기반 전세계 축구 정보 제공
전송 방식: stdio
명령어: python server_stdio.py
웹 검색 권한: ✅ 필수 활성화
```

## 💡 사용 예시

### 경기 결과 조회
```
"프리미어리그 지난 주 경기 결과 보여줘"
"맨체스터 유나이티드 최근 경기 어땠어?"
```

### 선수 정보 조회
```
"손흥민 선수 정보 알려줘"
"홀란드 이번 시즌 통계는?"
```

### 리그 순위 확인
```
"세리에A 현재 순위는?"
"분데스리가 상위 5팀 보여줘"
```

### 선수 비교
```
"홀란드랑 음바페 비교해줘"
"손흥민과 살라 누가 더 잘해?"
```

### 이적 소식
```
"프리미어리그 최근 이적 소식은?"
"레알 마드리드 영입 루머 알려줘"
```

## 🔍 웹 검색 기반

이 MCP는 **데이터베이스 없이 실시간 웹 검색**으로 작동합니다:

✅ 항상 최신 정보 제공
✅ 별도 API 키 불필요
✅ PlayMCP 웹 검색 권한만으로 완전 작동

## 📊 작동 방식

```
사용자 질문
    ↓
PlayMCP → MCP 서버 (stdio)
    ↓
도구 실행 (예: get_player_info)
    ↓
웹 검색 키워드 생성
    ↓
Claude ← "🔍 웹 검색이 필요합니다..."
    ↓
Claude가 자동으로 웹 검색 수행
    ↓
최신 정보 수집
    ↓
정리된 답변 제공
```

## 🎯 특징

- **실시간 정보**: 데이터베이스 없이 항상 최신 정보
- **다국적 지원**: 8개 주요 리그 커버
- **무료 운영**: API 키나 유료 서비스 불필요
- **PlayMCP 최적화**: 웹 검색 권한만으로 완전 작동

## 🔧 기술 스택

- **Protocol**: MCP (Model Context Protocol)
- **Transport**: stdio
- **Language**: Python 3.11+
- **Framework**: MCP SDK

## 📝 로컬 테스트

### 설치
```bash
pip install mcp
```

### 실행
```bash
python server_stdio.py
```

## 📦 GitHub 저장소

https://github.com/AlexAI-MCP/weekly-soccer-mcp

## 📄 라이선스

MIT License

## 🤝 기여

이슈 및 PR은 언제나 환영합니다!

## ⚽ 즐거운 축구 관전 되세요!
