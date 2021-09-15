# POAPbot

Bot which is able to send POAP links to eligible users 


## Installation
1. [Install Docker](https://docs.docker.com/engine/install/ubuntu/)
2. Copy and update settings in `.env.example`
3. Execute `docker-compose up -d`
4. Install requirements from `requirements.txt` for `>= Python 3.8`
5. Copy and update settings in `config.example.py`
6. Init database tables via `aerich upgrade`
7. Start bot via `python bot.py` or [via supervisord](http://supervisord.org/) or [systemd](https://es.wikipedia.org/wiki/Systemd)
8. Add a bot to the server with at least `3072` scope
