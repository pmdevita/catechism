# Catechism Online

A responsive website for reading the Catechism of the Catholic Church

The Catechism of the Catholic Church is a handbook that compiles and explains Church teaching on a wide variety 
of subjects. Unfortunately, as useful as this text is, it is not easily available to read. While the Vatican 
and USCCB each host their own version, both present a poor user experience making them sub-optimal both for 
general reading and reference.

Catechism Online is a web app designed for modern devices. It is designed for readability on any screen size and to 
be easily navigated, searched, and referenced.  

## Setup

### Requirements

- Node 10+
- Python 3.7+

### Front-end

```shell
cd www
npm i
npm run prod # modes listed in package.json
```

### Back-end

Create config.ini in root directory (see config.ini.example)

```shell
virtualenv venv
# or
python3 -m virtualenv venv
venv\Scripts\activate.bat
# or
source venv/bin/activate
pip install -r requirements.txt
flask run backend/app.py
```

## Hot reload mode

Run `npm dev-server` and set mode to `development` in config.ini for running with hot reload enabled

## Preact debugging

[Download here](https://github.com/preactjs/preact-devtools)

## Roadmap

[See Issue #1](https://github.com/pmdevita/catechism/issues/1)
