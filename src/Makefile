run:
	sudo python3 /home/ubuntu/HANKEN/src/HANKEN/manage.py runsslserver 172.31.5.170:443 --certificate /etc/letsencrypt/live/hanken.link/fullchain.pem --key /etc/letsencrypt/live/hanken.link/privkey.pem

migrate:
	python3 /home/ubuntu/HANKEN/src/HANKEN/manage.py migrate

test:
	python3 /home/ubuntu/HANKEN/src/HANKEN/manage.py test

superuser:
	sudo python3 /home/ubuntu/HANKEN/src/HANKEN/manage.py createsuperuser

clear:
	sudo python3 /home/ubuntu/HANKEN/src/HANKEN/manage.py clearsessions

rerease:
	python3 /home/ubuntu/HANKEN/src/HANKEN/manage.py collectstatic