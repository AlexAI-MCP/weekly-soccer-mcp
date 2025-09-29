# 🚨 Railway 환경 변수 설정 가이드

## 1단계: Railway 대시보드 접속

```
https://railway.app/dashboard
```

## 2단계: 프로젝트 선택

- "weekly-soccer-mcp" 클릭
- 또는 검색창에서 프로젝트 검색

## 3단계: Variables 탭

1. 좌측 메뉴에서 **"Variables"** 클릭
2. **"+ New Variable"** 버튼 클릭
3. 다음 정보 입력:

```
Variable Name: FOOTBALL_API_KEY
Value: 8acc268e54594f698d695ab84a9adc38
```

4. **"Add"** 또는 **"Save"** 클릭

## 4단계: 재배포 확인

- 환경 변수 추가 시 자동 재배포
- Deployments 탭에서 진행 상황 확인
- 보통 2-3분 소요

## 5단계: 테스트

```bash
# 헬스체크
curl https://web-production-137a.up.railway.app/

# 응답 예시:
{
  "status": "healthy",
  "service": "Weekly Soccer MCP v4.0",
  "api": "Football-Data.org",
  "timestamp": "2025-09-29T06:40:00.000000"
}
```

## 🔍 문제 해결

### ❌ 403 Forbidden 에러

**원인:** API 키가 설정되지 않음

**해결:**
1. Railway Variables 다시 확인
2. 값이 정확한지 확인: `8acc268e54594f698d695ab84a9adc38`
3. 재배포 대기 (2-3분)

### ❌ 429 Too Many Requests

**원인:** API 요청 제한 초과 (10 req/min)

**해결:**
- 잠시 대기 후 재시도
- 무료 플랜은 10 요청/분 제한

### ❌ 500 Internal Server Error

**원인:** 서버 코드 에러

**해결:**
1. Railway Logs 확인
2. GitHub 최신 커밋 확인
3. 재배포 시도

---

## ✅ 성공 확인 체크리스트

- [ ] Railway 환경 변수 `FOOTBALL_API_KEY` 설정 완료
- [ ] Railway 자동 재배포 완료 (Deployments 탭)
- [ ] 헬스체크 URL 접속 성공 (`status: healthy`)
- [ ] PlayMCP에 MCP 등록 (URL: `https://web-production-137a.up.railway.app/mcp`)
- [ ] PlayMCP에서 테스트 성공

---

## 📞 도움이 필요하면

1. Railway 로그 확인: `railway logs`
2. GitHub Issues: https://github.com/AlexAI-MCP/weekly-soccer-mcp/issues
3. Football-Data.org 상태: https://www.football-data.org/

---

Made with ⚽ for PlayMCP v4.0
