@echo off
echo ========================================
echo 위클리 해축 MCP - Railway 배포 스크립트
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Git 상태 확인...
git status

echo.
echo [2/5] 변경사항 커밋...
git add .
set /p commit_msg="커밋 메시지를 입력하세요 (엔터=자동): "
if "%commit_msg%"=="" set commit_msg=Update: 서버 업데이트
git commit -m "%commit_msg%"

echo.
echo [3/5] Railway 로그인 확인...
railway whoami
if errorlevel 1 (
    echo Railway 로그인이 필요합니다.
    railway login
)

echo.
echo [4/5] Railway 배포 시작...
railway up

echo.
echo [5/5] 도메인 정보 확인...
railway domain

echo.
echo ========================================
echo 배포 완료!
echo ========================================
echo.
echo 다음 URL을 PlayMCP에 등록하세요:
railway domain
echo.
pause
