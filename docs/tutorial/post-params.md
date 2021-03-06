# Partie 5 - POST data
> **Warning** : This project is private and is still in design, not ready for production. Create an issue if you encounter any bugs!

=== "templates/awesome_app/detail_film.html"
```html
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>{{ film.title }}</title>
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
		            <!-- film -->
		            <div class="comment">
		            	<form method="post">
		            		<div>
		            			<input type="text" name="name">
		            		</div>
		            		<div>
		            			<textarea rows="10" cols="50" name="comment"></textarea>
		            		</div>
		            		<input type="submit" class="button-favoir-and-details" value="Submit" style="font-size: 21px;">
		            	</form>
		            	<!-- list comment -->
		            </div>
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

=== "app/views.py"
```python
@router('/films/<int:id>', methods=['GET', 'POST'])
def film_detail(request, id):
    film = {
        'data': film for film in films if film['id'] == id
    }
    if not film.get('data'):
        return "Film does not exist"
    # post data
    if request.method == 'POST':
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        print(name, comment)
    contexts = {
        'film': film['data'],
    }
    return render('awesome_app/detail_film.html', contexts)
```
<hr/>
Continue to the tutorial <a href="https://docs.nimbasolution.com/tutorial/models/">Partie 6 - Models</a>