@echo off
echo Установка зависимостей...
python3 -m pip install -r requirements.txt
echo Запуск JonyaTooL...
python main.py
pause