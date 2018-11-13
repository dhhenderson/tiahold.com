# tiahold.com

## Prereqs

 * python3.6 (lambda supported version) (brew - use raw github link)
 * pipenv (install w/ pip3 b/c brew points it to python 3.7)
 * awscli (brew)
 * docker for mac (for local dev w/ dynamodb)

## Install

```
git clone https://github.com/dhhenderson/tiahold.com.git
cd tiahold.com
pipenv install --three
```

## Local dev

```
pipenv install --dev
pipenv shell
export FLASK_ENV=development
export APP_CONFIG_FILE=/path/to/config/development.py
docker run -p 8000:8000 amazon/dynamodb-local
flask init-db
python -m pytest -v
flask run
```
* Env vars can be put into .env file and pipenv shell will load

## Deploy

```
aws configure
zappa deploy production
```

## References

* http://exploreflask.com/en/latest/configuration.html
* https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
