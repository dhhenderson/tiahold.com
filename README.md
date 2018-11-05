# tiahold.com

## Prereqs

 * python3.6 (lambda supported version) (brew - use raw github link)
 * pipenv (install w/ pip3 b/c brew points it to python 3.7)
 * awscli (brew)
 * docker for mac (for local dev w/ dynamodb)

## Install

```bash
git clone https://github.com/dhhenderson/tiahold.com.git
cd tiahold.com
pipenv install --three
pipenv shell
```

## Local dev

```
docker run -p 8000:8000 amazon/dynamodb-local
export FLASK_APP=tiahold.py
export FLASK_ENV=development
flask initdb
flask run
```

## Deploy

```
aws configure
zappa deploy production
```
