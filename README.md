Для установки зависимостей: ```shell pip install -r requirements.txt```

Для запуска: ```shell uvicorn main:app --port 8080```

Перед запуском создайте в основной папке проекта файл .env и заполните его данными. Вот данные для тестового запуска:
```python
TOKEN_ADDRESS=0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0
POLYGON_RPC=https://polygon-rpc.com
API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6Ijg4N2I2ZjMyLTBhNDctNGY2Mi04MWZiLTMyMGM3ZjhjZGZhMiIsIm9yZ0lkIjoiNDgwNTc1IiwidXNlcklkIjoiNDk0NDE0IiwidHlwZUlkIjoiNWM0OTU0ZDgtYTM3ZC00MjVjLWFmNmMtZWRjNWQyMTU2NzVhIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NjI3ODY2MDMsImV4cCI6NDkxODU0NjYwM30.pmmZQLHa1IcdDeIB08kWEfjuzFi2iGpBzTTkBd3ermA
```