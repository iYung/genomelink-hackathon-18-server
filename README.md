# OAuth Example - Python Flask web app

[![CircleCI](https://circleci.com/gh/genomelink/oauth-example-flask.svg?style=svg)](https://circleci.com/gh/genomelink/oauth-example-flask)

## Requirements

- Python 2.7, 3.6
- Flask
- [genomelink](https://pypi.python.org/pypi/genomelink)

## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## How to run

### Register your app

Visit ["My apps"](https://genomelink.io/developers/apps/) console and set

- Name: as you like
- Redirect uris: `http://127.0.0.1:5000/callback`

Set scopes (whitelists) in "Authorization scopes" panel.

- [x] report:eye-color
- [x] report:beard-thickness
- [x] report:morning-person

### Run your app

```
$ export GENOMELINK_CLIENT_ID=<your_client_id>
$ export GENOMELINK_CLIENT_SECRET=<your_client_secret>
$ export GENOMELINK_CALLBACK_URL="http://127.0.0.1:5000/callback"
$ python app.py
```

then, visit `http://127.0.0.1:5000`

## How it works

See https://genomelink.io/developers/docs/tutorial-oauth-example/
