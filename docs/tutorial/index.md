# Parite 1 - Setup
> **Warning** : This project is private and is still in design, not ready for production. Create an issue if you encounter any bugs!

Make sure you have python3.6 +. Let's start by creating a virtual environment.

```sh
$ python --version
```

## Install Nimba
```sh
$ pip install nimba
```

## Create nimba application
```sh
$ nimba create --app awesome_app
```

### Structure project

* `app` - Your app project, you will spend most of your time here.
    - `views.py` - Your logic code
    - `models.py` - Define here the schema of your database
    - `tests.py` - Write your test here
* `staticfiles` - The static files.
* `templates` - Your template (html page etc...).
* `settings.py` - Settings database, secret key and other.
* `mask.py` - the command utility, start the server, create views and many more.


## Run server
In your project app `awesome_app`

```console
$ python mask.py serve

Monitoring for changes...
Starting server in PID 72932
June 25, 2021 - 18:04:32
Serving on http://127.0.0.1:8000
Quit the server with CONTROL-C.
```
Open <a href="http://127.0.0.1:8000" target="_blank">`http://127.0.0.1:8000`</a>

You cant change port with `python mask.py serve -p 7000` (runing with port 7000) <br/>
Or sharing ip `python mask.py serve -s 0:7000` (0.0.0.0:7000)

## Create other view
A view is a python function decorated with an url path, accepting a web request and returning a response. This response can contain html, template, xml etc.

A simple view returning html code with a decorate path. Open your `views.py` in your `app` folder
```python
from nimba.http import router

@router('/about')
def about(request):
	return "<h1> Hello, <h2> Welcom to my app page"
```

Each life is decorated by a road indicating a path

* `from nimba.http import router` 
* `@router('/about')` the router decorator makes your function a view, it receives web requests.
* `request` is the request web content all data get and post

Open <a href="http://127.0.0.1:8000/about" target="_blank">`http://127.0.0.1:8000/about`</a> <br/>
<hr/>
Continue to the tutorial <a href="https://docs.nimbasolution.com/tutorial/path-params/" target="_blank">Partie 2 - Endpoint</a>
