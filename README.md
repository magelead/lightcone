# Deploy a Flask APP on AWS EC2 with Gunicorn and Nginx


## Contents

- Develope and test your flask app locally
- Create a AWS EC2 and SSH into it
- Install softwares
- Transfer your project files to remote host (EC2)
- Install python packages
- Running a Flask app on a Gunicorn server
- Configuring Nginx to Proxy Requests
- Install SSL Certificate NGINX Server Steps (TODO)

## Develope and test your flask app locally
$ python3 main.py

## Create a AWS EC2 and SSH into it

https://www.twilio.com/blog/deploy-flask-python-app-aws 


## Install softwares

$ sudo apt-get update
$ sudo apt-get install nginx
$ sudo apt-get install python3-pip python3-dev


## Transfer your project files to remote host

Run following command from a local macine.

Push:

$ rsync -avL --progress -e "ssh -i ~/Documents/lightcone/lightcone.pem" ~/Documents/lightcone/ ubuntu@54.198.2.86:/home/ubuntu/lightcone/

Pull:

$ rsync -chavzP -e "ssh -i ~/Documents/lightcone/lightcone.pem" ubuntu@54.198.2.86:/home/ubuntu/lightcone/ ~/Documents/lightcone/

## Install python packages

$ python3 -m pip install -r requirements.txt

$ export PATH=$PATH:/home/ubuntu/.local/bin
(modify ~/.profile if you want)


## Running a Flask app on a Gunicorn server

$ gunicorn --bind 0.0.0.0:8080 main:app

The above command binds http://0.0.0.0:8080 to your flask app

Go to your browser again, you should see Hello World!

http://54.198.2.86:8080/

Ctrl+c to stop Gunicorn server.

Next, let’s create the systemd service unit file. 
Creating a systemd unit file will allow Ubuntu’s init system to automatically start Gunicorn and serve the Flask application whenever the server boots.

$ sudo vim /etc/systemd/system/lightcone.service

```
[Unit]
Description=Gunicorn
After=network.target


[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/lightcone
ExecStart=/home/ubuntu/.local/bin/gunicorn --workers 3 --bind unix:lightcone.sock -m 007 main:app


[Install]
WantedBy=multi-user.target

```

We can now start the Gunicorn service we created and enable it so that it starts at boot:

$ sudo systemctl start lightcone

$ sudo systemctl enable lightcone

$ sudo systemctl status lightcone


You now have a socket file, lightcone.sock, in the project directory.

And your flask app binds to lightcone.sock.

Whenever you modify /etc/systemd/system/lightcone.service, remember to reload it

$ sudo systemctl daemon-reload

Whenever you modify your project, remember to restart the Gunicorn service.

$ sudo systemctl restart lightcone


## Configuring Nginx to Proxy Requests

Our Gunicorn application server should now be up and running, waiting for requests on the socket file in the project directory. Let’s now configure Nginx to pass web requests to that socket by making some small additions to its configuration file.


$ sudo vim /etc/nginx/sites-available/lightcone


```
server {
    listen 80;
    server_name 54.198.2.86;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/lightcone/lightcone.sock;
    }
}
```

To enable the Nginx server block configuration you’ve just created, link the file to the sites-enabled directory:


$ sudo ln -s /etc/nginx/sites-available/lightcone /etc/nginx/sites-enabled


With the file in that directory, you can test for syntax errors:

$ sudo nginx -t

If this returns without indicating any issues, restart the Nginx process to read the new configuration:

$ sudo systemctl restart nginx

($ sudo systemctl stop nginx)

Go to your browser again, you should see Hello World!

http://54.198.2.86:80/

Port 80 is the default for http, which can be ommited.

http://54.198.2.86/

If you encounter any errors, trying checking the following:

checks the Nginx error logs

$ sudo less /var/log/nginx/error.log

checks the Nginx access logs

$ sudo less /var/log/nginx/access.log

checks the Nginx process logs

$ sudo journalctl -u nginx

checks your Flask app’s Gunicorn logs.

$ sudo journalctl -u lightcone



## Install SSL Certificate NGINX Server Steps

https://phoenixnap.com/kb/install-ssl-certificate-nginx

## Workflow 

Modify project, Test it locally, Transfer project to remote, Restart Gunicorn service.

