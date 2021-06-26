# Nimba framework
Nimba Framework is a modern, fast (coding), web framework with python.

<p align="center">
  <a href="https://docs.nimbasolution.com"><img src="https://github.com/hadpro24/nimba-framework/blob/main/docs/img/nimba-logo.png?raw=true" alt="Nimba Framework" style="width: 200px;"></a>
</p>

The key features are:

* **Fast to code**: Increase the speed to develop features. *
* **Intuitive**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging.
* **Easy**: Designed to be easy to use and learn. Less time reading docs.
* **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.

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

* `app` - Your app project, you will spend most of your time here.
    - `views.py` - Your logic code
    - `models.py` - Define here the schema of your database
    - `test.py` - Write your test here
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

## Licence

This project is licensed under the terms of Nimba solution compagny.


## Credit

Harouna Diallo
