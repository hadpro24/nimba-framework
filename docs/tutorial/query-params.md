# Partie 4 - Query parameters
> **Warning** : This project is private and is still in design, not ready for production. Create an issue if you encounter any bugs!

=== "templates/awesome_app/films.html"
```html
<!DOCTYPE html>
<html>
  <head>
    <title>My films</title>
  </head>
  <link rel="stylesheet" type="text/css" href="{{ load_static('awesome_app/css/main.css') }}">
  <body class="contenair">
    	<h1>List films</h1>
    	<div class="search-field">
	      <form>
	      	<input type="search" name="search" value="{{ search }}" placeholder="Search film with title...">
	      	<input type="submit" class="button-favoir-and-details" value="Search" style="font-size: 21px;">
	      </form>
	    </div>
    	<div class="films-list" >
    		{% if films %}
			    {% for film in films %}
				    <div class="card-film">
				    	<div class="image">
					    	<img 
					    			src="https://raw.githubusercontent.com/hadpro24/googlechallenge-phase-1-backend/master/media/{{ film.image }}" 
					    			alt="{{ film.title }}"/>
				    	</div>
				    	<div class="description">
					    	<h3>{{ film.title }}</h3>
					    	<h5><strong><em>Year of production : </em></strong>{{ film.released }}</h5>
					    	<div class="button-two">
					    		<a type="button" class="button-favoir-and-details" href="/films/{{ film.id }}">Details</a>
					    	</div>
				    	</div>
				    </div>
				  {% endfor %}
				{% else %}
					   <p>Not found, try other film title.</p>
				{% endif %}
    	</div>
  </body>
</html>

```

=== "app/views.py"
```python
from nimba.http import router, render

@router('/')
def home(request):
    search = request.GET.get('search', '')
    films_filter = [
        film for film in films if search in ' '.join(
            [film['title'], film['description'], film['country']]
        )
    ] if search else films
    contexts = {
        'films': films_filter,
        'search': search,
    }
    return render('awesome_app/list_films.html', contexts)

```

<hr/>
Continue to the tutorial <a href="https://docs.nimbasolution.com/tutorial/post-params/" target="_blank">Partie 5 - POST data</a>