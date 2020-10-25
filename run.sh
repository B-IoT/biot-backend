source .env/bin/activate 
cd backend
uvicorn main:app --reload --ssl-keyfile=../localhost-key.pem --ssl-certfile=../localhost.pem