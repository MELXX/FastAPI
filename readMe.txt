
run "docker build -t myBackend ." from ./BE docker build -t myBackend .

docker run -d --name myBackendContainer -p 80:80 myBackend

create a venv 
