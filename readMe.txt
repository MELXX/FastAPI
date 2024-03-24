
run "docker build -t mybackend ." from ./BE

docker run --network=mybridgenetwork -d --name myBackendContainer -p 8000:8000 mybackend

to run locally:
cd code
uvicorn main:app --reload

for docs
<app root>/docs e,g, http://127.0.0.1:8000/docs
