# 🚀 Railway 배포 가이드

## 📌 배포 전 체크리스트

✅ 로컬 테스트 완료  
✅ Git 저장소 초기화 완료  
✅ 모든 파일 커밋 완료  

---

## 🔧 Railway CLI 배포 (권장)

### 1단계: Railway 로그인
```bash
cd C:\Users\daewoo111\AppData\Local\AnthropicClaude\app-0.13.37\weekly-soccer-mcp
railway login
```
→ 브라우저가 열리면 Railway 계정으로 로그인

### 2단계: 프로젝트 초기화
```bash
railway init
```
- 프로젝트 이름: `weekly-soccer-mcp` (또는 원하는 이름)
- 엔터를 눌러 확인

### 3단계: 배포
```bash
railway up
```
→ 자동으로 Python 감지 후 배포 시작

### 4단계: 도메인 생성
```bash
railway domain
```
→ 공개 URL 자동 생성 (예: weekly-soccer-mcp-production.up.railway.app)

### 5단계: 배포 상태 확인
```bash
railway status
```

---

## 🌐 Railway 웹 대시보드 배포 (대안)

Railway CLI가 작동하지 않을 경우:

### 1. Railway 웹사이트 접속
https://railway.app → 로그인

### 2. 새 프로젝트 생성
- "New Project" 클릭
- "Deploy from GitHub repo" 선택
- GitHub에 코드 푸시 필요 시:

```bash
# GitHub 저장소 생성 후
cd C:\Users\daewoo111\AppData\Local\AnthropicClaude\app-0.13.37\weekly-soccer-mcp
git remote add origin https://github.com/YOUR_USERNAME/weekly-soccer-mcp.git
git push -u origin master
```

### 3. 저장소 선택
- 방금 생성한 `weekly-soccer-mcp` 저장소 선택

### 4. 자동 배포 확인
- Railway가 자동으로 Python 감지
- `railway.json` 설정대로 배포 시작

### 5. 도메인 설정
- 프로젝트 대시보드에서 "Settings" 탭
- "Generate Domain" 클릭
- 생성된 URL 복사

---

## 📡 PlayMCP 연결

### 배포 후 URL 형식
```
https://your-app-name.up.railway.app/mcp
```

### PlayMCP 설정
1. PlayMCP 접속
2. "Add Server" 클릭
3. 정보 입력:
   - **Name**: 위클리 해축
   - **URL**: `https://your-app-name.up.railway.app/mcp`
   - **웹 검색 권한**: ✅ 활성화
   - **이미지 분석**: ❌ 비활성화

4. "Save" 클릭

---

## 🧪 배포 테스트

### 헬스 체크
```bash
curl https://your-app-name.up.railway.app/
```

응답 예시:
```json
{
  "status": "healthy",
  "server": "위클리 해축 MCP",
  "version": "1.0.0",
  "supported_leagues": [...],
  "tools_count": 9
}
```

### MCP 초기화 테스트
```bash
curl -X POST https://your-app-name.up.railway.app/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize"}'
```

---

## 💡 PlayMCP에서 테스트할 질문들

1. **경기 결과 조회**
   ```
   "프리미어리그 지난 주 경기 결과 보여줘"
   "토트넘 최근 7일 경기 어땠어?"
   ```

2. **선수 정보**
   ```
   "손흥민 선수 정보 알려줘"
   "홀란드 이번 시즌 통계는?"
   ```

3. **리그 순위**
   ```
   "세리에A 현재 순위 보여줘"
   "K리그1 상위 5팀은?"
   ```

4. **선수 비교**
   ```
   "손흥민과 살라 비교해줘"
   "음바페 vs 홀란드 누가 더 잘해?"
   ```

5. **경기 일정**
   ```
   "프리미어리그 이번 주 경기 일정은?"
   "맨체스터 시티 다음 경기는?"
   ```

6. **득점왕**
   ```
   "라리가 득점왕 순위 보여줘"
   "분데스리가 상위 득점자는?"
   ```

---

## 🔍 문제 해결

### Railway 로그 확인
```bash
railway logs
```

### 재배포
```bash
git add .
git commit -m "Fix: 문제 수정"
railway up
```

### 환경 변수 확인 (필요시)
```bash
railway variables
```

---

## 📊 배포 상태 모니터링

Railway 대시보드에서 확인 가능:
- CPU 사용률
- 메모리 사용량
- 요청 수
- 에러 로그

---

## 🎉 배포 완료!

다음 URL이 생성됩니다:
```
https://weekly-soccer-mcp-production.up.railway.app/mcp
```

이 URL을 PlayMCP에 등록하면 사용 준비 완료! ⚽
스트
다음 질문으로 테스트:
```
"프리미어리그 지난 주 경기 결과 보여줘"
"손흥민 선수 정보 알려줘"
"세리에A 현재 순위는?"
```

---

## 🧪 로컬 테스트 결과

### ✅ 헬스 체크 성공
```json
{
  "status": "healthy",
  "server": "위클리 해축 MCP",
  "version": "1.0.0",
  "supported_leagues": [...],
  "tools_count": 9
}
```

### ✅ MCP 초기화 성공
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {"tools": {}},
    "serverInfo": {
      "name": "weekly-soccer-mcp",
      "version": "1.0.0"
    }
  }
}
```

---

## 💡 작동 원리

### 웹 검색 트리거 방식
모든 도구는 Claude에게 **웹 검색 요청**을 생성합니다:

```python
# 예시: get_recent_matches 도구
return f"""🔍 웹 검색이 필요합니다:

**검색 키워드**: 프리미어리그 경기 결과 2025년 9월 22일 ~ 29일

**찾아야 할 정보**:
1. 날짜별 경기 결과
2. 홈팀 vs 원정팀
3. 최종 스코어
4. 주요 득점자
"""
```

Claude가 이 응답을 받으면:
1. 자동으로 웹 검색 수행
2. 최신 정보 수집
3. 정리된 결과 제공

---

## 🔒 보안 및 성능

### 환경 변수
```python
port = int(os.environ.get("PORT", 8080))
```
Railway가 자동으로 PORT 할당

### CORS 설정
```python
app.add_middleware(CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```
PlayMCP와의 통신 허용

### 에러 처리
```python
try:
    # 도구 실행
except Exception as e:
    return f"❌ 오류 발생: {str(e)}"
```

---

## 📊 예상 사용 시나리오

### 시나리오 1: 주말 경기 리뷰
```
사용자: "프리미어리그 이번 주말 경기 어땠어?"
→ get_recent_matches(league="프리미어리그")
→ 웹 검색으로 최신 결과 제공
```

### 시나리오 2: 선수 분석
```
사용자: "손흥민이랑 살라 누가 더 잘해?"
→ compare_players(player1="손흥민", player2="살라")
→ 양쪽 통계 검색 후 비교표 생성
```

### 시나리오 3: 리그 현황 파악
```
사용자: "세리에A 현재 1위는?"
→ get_league_standings(league="세리에A", top_n=5)
→ 최신 순위표 검색 후 제공
```

### 시나리오 4: 이적 시장 추적
```
사용자: "최근 프리미어리그 이적 소식 있어?"
→ get_transfer_news(league="프리미어리그")
→ 지난 7일 이적 뉴스 검색
```

---

## 🔄 업데이트 및 유지보수

### 코드 수정 후 재배포
```bash
cd C:\Users\daewoo111\AppData\Local\AnthropicClaude\app-0.13.37\weekly-soccer-mcp
git add .
git commit -m "Update: 기능 개선"
railway up
```

### 로그 확인
```bash
railway logs
```

### 상태 모니터링
```bash
railway status
```

---

## 📚 추가 기능 아이디어

향후 추가 가능한 도구들:

1. **get_head_to_head**
   - 두 팀의 과거 전적 비교

2. **get_injury_news**
   - 최근 부상자 명단

3. **get_referee_stats**
   - 심판 통계 (카드 발급률 등)

4. **get_betting_odds**
   - 베팅 오즈 정보 (참고용)

5. **get_youth_players**
   - 유망주 정보

---

## 🎯 성공 체크리스트

### 개발 완료
- [x] 9개 도구 구현
- [x] MCP 프로토콜 준수
- [x] 웹 검색 트리거 설계
- [x] 에러 처리 구현

### 테스트 완료
- [x] 로컬 서버 실행 성공
- [x] 헬스 체크 작동
- [x] MCP 엔드포인트 응답
- [x] Git 저장소 생성

### 배포 준비
- [x] requirements.txt
- [x] Procfile
- [x] railway.json
- [x] README.md
- [x] DEPLOYMENT.md
- [x] deploy.bat

---

## 🌟 핵심 강점

### 1. 데이터베이스 불필요
모든 정보를 실시간 웹 검색으로 수집
→ 항상 최신 정보 보장

### 2. 다국적 리그 지원
8개 주요 리그 커버
→ 글로벌 축구 팬 대응

### 3. 즉시 배포 가능
Railway 무료 플랜 활용
→ 추가 비용 없음

### 4. PlayMCP 최적화
웹 검색 권한만으로 작동
→ 설정 간단

---

## 🏁 다음 단계

### 1. Railway 배포
```bash
deploy.bat
```
실행하여 5분 안에 배포 완료

### 2. URL 확인
Railway에서 생성된 MCP 엔드포인트 복사

### 3. PlayMCP 등록
URL 입력 + 웹 검색 권한 활성화

### 4. 테스트
샘플 질문으로 작동 확인

### 5. 피드백 수집
실제 사용 후 개선점 파악

---

## 📞 문제 발생 시

### Railway 배포 실패
1. `railway logs` 확인
2. Python 버전 확인 (3.11+ 권장)
3. requirements.txt 재확인

### MCP 연결 실패
1. URL 형식 확인 (`/mcp` 포함)
2. 웹 검색 권한 활성화 확인
3. Railway 서버 상태 확인

### 도구 작동 안됨
1. PlayMCP에서 웹 검색 권한 재확인
2. 도구 응답에서 검색 키워드 확인
3. Claude가 검색을 수행하는지 확인

---

## 🎉 축하합니다!

**위클리 해축 MCP 서버**가 완성되었습니다!

이제 Railway에 배포하고 PlayMCP에서 사용하시면 됩니다.

**배포 명령어 한 줄:**
```bash
cd C:\Users\daewoo111\AppData\Local\AnthropicClaude\app-0.13.37\weekly-soccer-mcp && deploy.bat
```

⚽ 행운을 빕니다! ⚽
