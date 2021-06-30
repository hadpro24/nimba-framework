# Partie 2 - Endpoint
> **Warning** : This project is private and is still in design, not ready for production. Create an issue if you encounter any bugs!


=== "app/views.py" 
```python
from nimba.http import router, render

articles = [
	{
		"id": 1,
		"title": "",
		"image": "",
		"description": "",
		"created_at": "",
	},
	{
		"id": 2,
		"title": "",
		"image": "",
		"description": "",
		"created_at": "",
	},
	{
		"id": 3,
		"title": "",
		"image": "",
		"description": "",
		"created_at": "",
	},
]

@router('/articles')
def list_articles(request):
	contexts = {
		'articles': articles
	}
	return render('awesome_app/articles.html', contexts)

```

=== "templates/awesome_app/articles.html" 
```jinja2
<!DOCTYPE html>
<html>
  <head>
    <title>My articles</title>
  </head>
  <body>
    <h1>List articles</h1>
	    {% for article in articles %}
		    <div>
		    	<h2> {{ article.title }} </h2>
		    	<img src="{{ article.image }}" alt="{{ article.title }}"/>
		    	<h3> Poster a {{ format_date(article.created_at) }} </h3>
		    	<p> {{ short_text(article.description, 20) }}</p>
		    	<a href="{{ url('article', id=article.id) }}">see more details</a>
		    </div>
		{% endfor %}
  </body>
</html>
```

=== "app/views.py"
```python
from nimba.http import router, render

@router('/articles/<id:int>')
def article(request, id):
	#articles variable exists
	article = [
		article for article in article if article['id'] == id
	]
	contexts = {
		'article': article,
	}
	return render('awesome_app/article.html', article)

```

```python
@router('/articles/<id:int>')
```


=== "templates/awesome_app/article.html" 
```jinja2
<!DOCTYPE html>
<html>
  <head>
    <title>{{ article.title }}</title>
  </head>
  <body>
    <h1>{{ article.title }}</h1>
    <div>
    	<img src="{{ article.image }}" alt="{{ article.title }}"/>
    	<h3> Poster a {{ format_date(article.created_at) }} </h3>
    	<p> {{ article.description }}</p>
    </div>
  </body>
</html>
```

<hr/>
Continue to the tutorial <a href="https://docs.nimbasolution.com/query-params/" target="_blank">Partie 3 - Query parameters</a>