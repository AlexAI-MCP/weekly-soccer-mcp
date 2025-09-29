# 위클리 해축 MCP - stdio 방식 배포 가이드

## 🎯 개요

위클리 해축 MCP는 K-Beauty MCP와 동일한 **stdio 방식**으로 작동합니다.

## 📋 stdio 방식이란?

- **Standard Input/Output** 방식
- 명령줄에서 직접 실행
- HTTP 서버 불필요
- PlayMCP가 프로세스를 직접 관리

## 🚀 PlayMCP 등록 방법

### 1단계: PlayMCP 콘솔 접속

https://playmcp.kakao.com/console

### 2단계: 새 MCP 서버 등록

**"새로운 MCP 서버 등록"** 클릭

### 3단계: 서버 정보 입력

#### 기본 정보
```
서버명: 위클리 해축
설명: 실시간 웹 검색 기반 전세계 축구 정보 (프리미어리그, 라리가, 세리에A, 분데스리가, K리그, J리그, MLS 등 8개 리그 지원)
```

#### 전송 방식
```
방식: stdio
```

#### 실행 명령어
```
python server_stdio.py
```

또는 GitHub에서 직접 설치하는 경우:
```
git clone https://github.com/AlexAI-MCP/weekly-soccer-mcp.git
cd weekly-soccer-mcp
pip install -r requirements.txt
python server_stdio.py
```

#### 권한 설정
```
웹 검색: ✅ 필수 활성화
이미지 분석: ❌ 불필요
```

### 4단계: 저장 및 심사 요청

"저장" 클릭 → "심사 요청" 클릭

## 🧪 테스트 방법

### PlayMCP에서 테스트

등록 후 PlayMCP AI 채팅에서:

```
"프리미어리그 지난 주 경기 결과 보여줘"
"손흥민 선수 정보 알려줘"
"세리에A 현재 순위는?"
"홀란드와 음바페 비교해줘"
```

### 로컬 테스트

```bash
# 1. 저장소 클론
git clone https://github.com/AlexAI-MCP/weekly-soccer-mcp.git
cd weekly-soccer-mcp

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 서버 실행
python server_stdio.py
```

stdio 방식이므로 직접 입력/출력으로 테스트할 수 있습니다.

## 📊 stdio vs HTTP 비교

| 항목 | stdio 방식 | HTTP 방식 |
|------|-----------|-----------|
| 실행 방식 | 명령줄 프로세스 | 웹 서버 |
| 배포 | 불필요 | Railway/Render 필요 |
| URL | 없음 | 필요 |
| 설정 | 간단 | 복잡 |
| PlayMCP 통합 | 직접 실행 | URL 연결 |

## ✅ 장점

### stdio 방식의 장점
- ✅ 배포 서버 불필요
- ✅ 설정이 간단
- ✅ 로컬 실행 가능
- ✅ PlayMCP가 직접 관리
- ✅ 비용 없음

## 🔧 작동 원리

```
PlayMCP 콘솔
    ↓
서버 등록 (stdio)
    ↓
PlayMCP가 server_stdio.py 실행
    ↓
사용자 질문 → MCP 서버
    ↓
웹 검색 요청 생성
    ↓
Claude가 웹 검색 수행
    ↓
결과 반환
```

## 🎯 K-Beauty와 비교

| 항목 | K-Beauty MCP | 위클리 해축 MCP |
|------|--------------|----------------|
| 전송 방식 | stdio | stdio |
| 실행 명령 | python server.py | python server_stdio.py |
| 웹 검색 | 필요 | 필요 |
| 도구 수 | 9개 | 9개 |
| 주제 | 뷰티 | 축구 |

## 📝 주의사항

### 필수 요구사항
1. Python 3.11 이상
2. mcp 패키지 설치
3. PlayMCP 웹 검색 권한 활성화

### 일반적인 문제

#### 문제 1: 모듈을 찾을 수 없음
```
ModuleNotFoundError: No module named 'mcp'
```

**해결**:
```bash
pip install mcp
```

#### 문제 2: 웹 검색이 작동하지 않음
**해결**: PlayMCP 설정에서 웹 검색 권한 활성화 확인

#### 문제 3: 응답이 없음
**해결**: stdio 방식이므로 PlayMCP가 프로세스를 직접 관리합니다. 등록 정보 확인

## 🔄 업데이트 방법

### GitHub에서 업데이트

```bash
cd weekly-soccer-mcp
git pull origin main
pip install -r requirements.txt --upgrade
```

### PlayMCP에서 재시작

PlayMCP 콘솔 → 위클리 해축 → "재시작"

## 📞 문의 및 지원

- GitHub Issues: https://github.com/AlexAI-MCP/weekly-soccer-mcp/issues
- PlayMCP 문의: https://playmcp.kakao.com

## 🎉 완료!

stdio 방식으로 간단하게 배포가 완료되었습니다!

이제 PlayMCP에서 위클리 해축 MCP를 사용할 수 있습니다! ⚽
