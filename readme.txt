357  ls
  358  clear
  359  ls
  360  cd Musical-App/
  361  ls
  362  cd ..
  363  ls
  364  clear
  365  ls
  366  ng build --prod
  367  ls
  368  clear
  369  ls
  370  cd Musical-App/
  371  ls
  372  pwd
  373  cd ..
  374  sudo nano Caddyfile 
  375  ls
  376  cd Musical-App/
  377  ls
  378  sudo nano Caddyfile
  379  ls
  380  clear
  381  ls
  382  sudo nano Caddyfile 
  383  caddy run
  384  sudo nano Caddyfile 
  385  cd ..
  386  ls
  387  cat Caddyfile 
  388  cd Musical-App/
  389  ls
  390  sudo nano Caddyfile 
  391  caddy run
  392  caddy run Caddyfile
  393  caddy adapt --config Caddyfile
  394  caddy adapt --config Caddyfile --validate
  395  caddy run
  396  clear
  397  ls
  398  cd ..
  399  ls
  400  sudo nano Dockerfile
  401  ls
  402  sudo nano docker-compose.yml
  403  ls
  404  docker
  405  sudo apt  install docker.io
  406  docker-compose
  407  sudo apt  install docker-compose
  408  ls
  409  docker compose -up
  410  docker--compose up
  411  docker-compose up
  412  ls
  413  sudo nano docker-compose.yml
  414  sudo nano Dockerfile 
  415  sudo nano docker-compose.yml
  416  docker-compose up
  417  docker
  418  docker ps
  419  sudo docker ps
  420  sudo docker-compose up
  421  ls
  422  cd venv/
  423  ls
  424  cd lib/
  425  ls
  426  cd ..
  427  ls
  428  sudo naon Dockerfile 
  429  sudo nano Dockerfile 
  430  sudo docker-compose up
  431  ls
  432  source venv/bin/activate
  433  pip freeze > requirements.txt
  434  sudo pip freeze > requirements.txt
  435  sudo pip freeze
  436  pip3 freeze
  437  sudo pip3 freeze > requirements.txt
  438  sudo nano requirements.txt 
  439  sudo docker-compose up
  440  sudo docker-compose up --no-cache
  441  sudo docker-compose build
  442  curl localhost:8000
  443  curl localhost:8000/ankushsir
  444  nginx
  445  sudo apt install nginx-core
  446  sudo service nginx status
  447  sudo service nginx enable
  448  sudo service nginx start
  449  caddy delete
  450  sudo apt remove caddy
  451  caddy
  452  sudo service nginx start
  453  sudo service nginx status
  454  sudo nano /etc/nginx/sites-available/musical-portal
  455  sudo rm /etc/nginx/sites-available/default 
  456  sudo ln -s /etc/nginx/sites-available/musical-portal /etc/nginx/sites-enabled/
  457  sudo service nginx reload 
  458  sudo nginx -t
  459  sudo rm /etc/nginx/sites-enabled/default 
  460  sudo service nginx reload 
  461  sudo docker-compose up -d
  462  ls
  463  sudo nano /etc/nginx/sites-available/musical-frontend
  464  sudo ln -s /etc/nginx/sites-available/musical-frontend /etc/nginx/sites-enabled
  465  sudo service nginx reload 
  466  curl localhost:8080
  467  history
(venv) ubuntu@ip-172-31-30-163:/home/deploy/musicbackend$ ls
Caddyfile   Musical-App  api         docker-compose.yml  media    music_portal      staticfiles  users
Dockerfile  Procfile     db.sqlite3  manage.py           modules  requirements.txt  templates    venv
(venv) ubuntu@ip-172-31-30-163:/home/deploy/musicbackend$ 


=========================================
Ankush Verma11:21 PM
:2015 {
    root ./
}
Ankush Verma11:28 PM
caddy adapt --config Caddyfile
caddy adapt --config Caddyfile --validate
Ankush Verma11:33 PM
FROM python:3.5.2
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
Dockerfile
Ankush Verma11:35 PM
version: '3'

services:
  web:
    image: django_local:latest
    container_name: prod_backend
    command: python3 manage.py runserver --settings=makerobos.production 0.0.0.0:8000
    ports:
      - "8000:8000"
    network_mode: "host"
    env_file:
     - ./prod.env
    depends_on:
      - "migration"

  migration:
    build: .
    image: django_local
    container_name: prod_image
    network_mode: "host"
    env_file:
     - ./prod.env
    volumes:
      - .:/code/

Ankush Verma12:00 AM
sudo apt remove package_name.
Ankush Verma12:03 AM
server {
    server_name 34.193.17.233;

    location / {
        proxy_pass http://0.0.0.0:8000$request_uri;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect     off;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;
    }

    
Ankush Verma12:11 AM
server {
    listen 80;
    server_name sample.com .sample.com;
    index index.html;
    root /usr/share/nginx/sample/dist;
    location / {
        try_files $uri$args $uri$args/ /index.html;
    }
}



=======Use Python3.6=======