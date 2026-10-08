@echo off
title PARISA HOME - Creating Comfort Marketplace
echo ========================================================
echo   PARISA HOME - PREMIUM HOME TEXTILES & LOUNGEWEAR
echo   Uzum Nasiya, Click, Payme & Parisa AI Assistant
echo ========================================================
echo.
echo Server ishga tushirilmoqda...
cd /d "E:\parisa_home_marketplace"
start http://127.0.0.1:8001
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
pause
