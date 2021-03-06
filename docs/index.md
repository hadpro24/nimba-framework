# Nimba framework
<p align="center">
  <a href="https://docs.nimbasolution.com"><img src="https://github.com/hadpro24/nimba-framework/blob/main/docs/img/nimba-logo.png?raw=true" alt="Nimba Framework" style="width: 200px;"></a>
</p>
> **warning** This project is private and is still in design, not ready for production. Create an issue if you encounter any bugs!

Nimba is a python web framework for lazy developers, just focus on your codes.

Everything you need to know about Nimba Framework
The key features are:

* **Fast to code**: Increase the speed to develop features.
* **Intuitive**: Quick understanding. Less debugging time..
* **Easy**: Designed to be easy to use and learn. Less time reading docs.
* **Short**: Minimizes code duplication. Multiple functionalities. Fewer bugs.

## Installation

<div class="termy">

```console
$ pip install nimba
```

</div>

## Create Application

<div class="termy">

```console
$ nimba create --app awesome_app
```

</div>

### Structure project

* `application` - Your app project (you will spend most of your time here).
    - `views.py` - Your logic code
    - `models.py` - Define here the schema of your database
    - `tests.py` - Write your test here
* `staticfiles` - The static files.
* `templates` - Your template (html page etc...).
* `settings.py` - Settings database, secret key and other.
* `mask.py` - the command utility, start the server, create views and many more.

## Run server
In your project app `awesome_app`
<div class="termy">

```console
$ python mask.py serve

Monitoring for changes...
Starting server in PID 72932
June 25, 2021 - 18:04:32
Serving on http://127.0.0.1:8000
Quit the server with CONTROL-C.
```

</div>

Open <a href="http://127.0.0.1:8000" target="_blank">`http://127.0.0.1:8000`</a> in your navigator
![Screenshot](https://github.com/hadpro24/nimba-framework/blob/main/result.png?raw=true)

Continue directly with <a href="https://docs.nimbasolution.com/tutorial">tutorial</a>

## Licence

This project is licensed under the terms of Nimba solution compagny.

