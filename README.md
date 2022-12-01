# CPSC449Project2

## Members of Team: 
Alejandro Ramos, Shreya Bhattacharya, Dillon Go, Manan Patel

## Introduction:
The goal is to split the monolith service created in Project 1(Wordle) into two seperate services User and Games and authenticating endpoints. In previous version we used HTTP basic authentication for signin endpoint but rest of the endpoints of games remained unauthenticated.
So, here we are using nginx reverse proxy to handle authentication.It will also act as API gateway for directing respective traffic, load balancing and authenticating request to game service.

## Steps to run our program:
1. Navigate to the correct directory of the project file. 
2. To initialize the database, we will run it by running these lines of code:
```
./bin/init.sh
```
3. Configure Nginx:
```
cd /etc/nginx/sites-enabled
sudo "${EDITOR:-vi}" tutorial
```
Then paste code in the "Nginx Configuration section, then run:
```
sudo service nginx restart
```
4. For logging, create a .env file with this inside:
```
QUART_ENV=development
```
5. To start the service, run this line of code:
```
foreman start -m game=3, user=1
```
## Database:
 The var folder holds two Databases:
 1. game.db
 2. user.db


1. game.db contains following tables:
Game,in_progress,Completed,Guessses,Correct_words,valid_words

2. user.db contains following tables:
 User table(containing username & password)
## Functionality
1. Splitting the monolith service into user & game
2. Authenticating endpoints(via nginx reverse proxy)
3. Load balancing
4. Directing traffic

## Nginx Configuration:
-configuring nginx to load balance between three games service
-setting up the server_name pointing to tuffix-vm(in case of Tuffix 2020 VM) 
-authenticating based on subrequest
```
upstream gameLoad{
         server 127.0.0.1:5000;
         server 127.0.0.1:5001;
         server 127.0.0.1:5002;
}

server {
       listen 80;
       listen [::]:80;

       server_name tuffix-vm;
       
       location / {
                  proxy_pass http://gameLoad;
                  auth_request /auth;
                  auth_request_set $auth_status $upstream_status;
       }
       
       location /user{
                  proxy_pass http://127.0.0.1:5100;
       }   

       location = /auth {
                  internal;
                  proxy_pass http://127.0.0.1:5100;
                  proxy_pass_request_body off;
                  proxy_set_header Content-Length "";
                  proxy_set_header X-Original-URI $request_uri;
       }
}
```

