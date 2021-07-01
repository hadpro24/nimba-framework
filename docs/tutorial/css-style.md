# Partie 3 - CSS and JavaScript

> **Warning** : This project is private and is still in design, not ready for production. Create an issue if you encounter any bugs!

=== "templates/awesome_app/films.html" 
```html
<!DOCTYPE html>
<html>
  <head>
    <title>My articles</title>
    <link rel="stylesheet" type="text/css" href="{{ load_static('awesome_app/css/main.css') }}">
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

=== "templates/awesome_app/film_detail.html" 
```html
<!DOCTYPE html>
<html>
  <head>
    <title>{{ article.title }}</title>
    <link rel="stylesheet" type="text/css" href="{{ load_static('awesome_app/css/main.css') }}">
	<style type="text/css">
		.contenair{
		  width: 85%;
		  margin:0 auto;
		  margin-top: 40px;

		  display: flex;
		  justify-content: space-between;
		  font-family: helvetica, tahoma, sans-serif;
		  text-align: left;
		}
		.data-film{
		  display: flex;
		}

		.info p{
		  line-height: 27px;
		}
		.info p span{
		    display: block;
		}
		.info p h3{
		  display: inline-block;
		}
		.couverture{
		  margin-left: 50px;
		}
	</style>
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

In the part, we code the links in hard. we are going to change that.

<hr/>
Continue to the tutorial <a href="https://docs.nimbasolution.com/query-params/" target="_blank">Partie 4 - Query parameters</a>
