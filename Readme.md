# Catechism Online

A responsive website for reading the Catechism of the Catholic Church

Right now, the official online sources for the CCC are all derived from the Vatican's, which was made over two decades 
ago, or the USCCB's which is a Flash application. This is intended to be a responsive HTML5 reader of the CCC with 
modern design practices for the best user experience.

We are currently in planning stages but since this is conceptually a simple web app, we are keeping things simple. 
We are using Flask on the backend for serving verses. The frontend will be built with vanilla ES6 for speed and Sass. 
More planning coming eventually.

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

```shell
cd backend
virtualenv venv
# or
python3 -m virtualenv venv
venv\Scripts\activate.bat
# or
source venv/bin/activate
pip install -r requirements.txt
```
