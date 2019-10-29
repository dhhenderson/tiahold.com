# tiahold.com

## Prereqs

 * pyenv (brew)
 * pipenv (brew)
 * awscli (brew)
 * docker for mac (for local dev w/ dynamodb)
 * # https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html

## Install

```
git clone https://github.com/dhhenderson/tiahold.com.git
cd tiahold.com
pyenv install 3.7.4
pyenv local 3.7.4
pipenv install
```

## Local dev

```
pipenv install --dev
pipenv shell
export FLASK_ENV=development
export APP_CONFIG_FILE=/abs/path/to/config/development.py
# ./xray_mac -o -n us-east-1
aws configure
docker run -p 8000:8000 amazon/dynamodb-local
flask init-db
python -m pytest -v
flask run
```
* Env vars can be put into .env file and pipenv shell will load
* boto requires aws config to be setup (region) even when just using dynamodb-local

## Deploy

```
aws configure
zappa deploy production
```

## References

* https://hackernoon.com/reaching-python-development-nirvana-bb5692adf30c
* https://dev.to/writingcode/the-python-virtual-environment-with-pyenv-pipenv-3mlo
* https://pipenv.kennethreitz.org/en/latest/basics/#general-recommendations-version-control
* http://exploreflask.com/en/latest/configuration.html
* https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
