# Nimba framework
Everything you need to know about Nimba Framework


Nimba Framework is a modern, fast (coding), web framework with Python 3.6+.

The key features are:

* **Fast to code**: Increase the speed to develop features. *
* **Intuitive**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging.
* **Easy**: Designed to be easy to use and learn. Less time reading docs.
* **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.

## Installation

<div class="termy">

```console
$ pip install nimba-framework
```

</div>

## Create Application

<div class="termy">

```console
$ nimba create --app awesome_app
```

</div>

### Structure project

* `app` - Create a new project.
    - `views.py` - views
    - `models.py` - views
    - `test.py` - test
* `staticfiles` - Start the live-reloading docs server.
* `templates` - Build the documentation site.
* `settings.py` - Print help message and exit.
* `mask.py` - Print help message and exit.

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

`` Open http://127.0.0.1:8000 in your navigator ``
![Screenshot](https://github.com/hadpro24/nimba-framework/blob/main/result.png?raw=true)

## Licence

This project is licensed under the terms of Nimba solution compagny.

