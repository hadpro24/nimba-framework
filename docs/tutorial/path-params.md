# Partie 2 - Endpoint
> **Warning** : This project is private and is still in design, not ready for production. Create an issue if you encounter any bugs!


=== "app/views.py" 
```python
from nimba.http import router, render

films = [
    {
        "id": 1,
        "title": "Dawn of the Planet of the Apes",
        "released": "2016-10-10",
        "description": "A group of scientists in San Francisco struggle to stay alive in the aftermath of a plague that is wiping out humanity, while Caesar tries to maintain dominance over his community of intelligent apes",
        "runtime": "02:00:00",
        "country": "French",
        "rated": "9.10",
        "image": "films/c6b7a11f-d1cb-427f-b784-4475f033fc48_1_gxBKoUN.png"
    },
    {
        "id":2,
        "title": "X-Men: Days of Future Past",
        "released": "2016-10-16",
        "description": "The ultimate X-Men ensemble fights a war for the survival of the species across two time periods as they join forces with their younger selves in an epic battle that must change the past – to save our future.",
        "runtime": "01:55:00",
        "country": "USA",
        "rated": "6.42",
        "image": "films/652565bb-02ad-487f-929e-78308085ca1e_4.jpg"
    },
    {
        "id": 3,
        "title": "Despicable Me 2",
        "released": "2013-10-02",
        "description": "Gru is recruited by the Anti-Villain League to help deal with a powerful new super criminal.",
        "runtime": "02:05:00",
        "country": "USA",
        "rated": "7.50",
        "image": "films/43b8cf94-8074-4e72-b58f-de6a3d067464_11.jpg"
    },
    {
        "id": 4,
        "title": "A Bug's Life",
        "released": "1998-10-04",
        "description": "On behalf of \"oppressed bugs everywhere,\" an inventive ant named Flik hires a troupe of warrior bugs to defend his bustling colony from a horde of freeloading grasshoppers led by the evil-minded Hopper.",
        "runtime": "01:56:40",
        "country": "Spanish",
        "rated": "7.00",
        "image": "films/92b4aed5-ef06-4065-af9a-1bb65e3d36d5_13.jpg"
    },
]

@router('/')
def list_films(request):
	contexts = {
		'films': films
	}
	return render('awesome_app/films.html', contexts)

```

=== "templates/awesome_app/films.html" 
```html
<!DOCTYPE html>
<html>
  <head>
    <title>My articles</title>
  </head>
  <body>
    <h1>List films</h1>
	<div class="films-list" >
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
	</div>
  </body>
</html>
```

=== "app/views.py"
```python
from nimba.http import router, render

@router('/films/<id:int>')
def film_detail(request, id):
	#films variable exists
	film = {
        'data': film for film in films if film['id'] == id
    }
    if not film.get('data'):
        return "Film does not exist"
	contexts = {
		'film': film['data'],
	}
	return render('awesome_app/film_detail.html', film)

```

```python
@router('/films/<id:int>')
```


=== "templates/awesome_app/film_detail.html" 
```html
<!DOCTYPE html>
<html>
  <head>
    <title>{{ article.title }}</title>
  </head>
  <body>
    <div class="contenair">
		<div class="data-film">
		     <div class="info">
		          <a href="/films">Back to list</a>
		          <h1>{{ film.title }}</h1>
		            <p>
		                {{ film.description }}
		            </p>
		            <p>
		                <span><strong>Released to : </strong> {{ film.released }}</span>
		                <span><strong>Runtime : </strong> {{ film.runtime }}</span>
		                <span><strong>Rated : </strong> {{ film.rated }}</span>
		                <span><strong>Languages : </strong> {{ film.country }}</span>
		            </p>
		     </div>
		     <div class="image">
		        <div class="couverture">
		          <img src="https://raw.githubusercontent.com/hadpro24/googlechallenge-phase-1-backend/master/media/{{ film.image }}" 
		          alt="{{ film.title }}" width="450">
		        </div>
		     </div>
		</div>
	</div>
  </body>
</html>
```

<hr/>
Continue to the tutorial <a href="https://docs.nimbasolution.com/tutorial/query-params/">Partie 3 - Query parameters</a>