from nimba.http import router, render, json_render

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

@router('/', name='home')
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

@router('/films/<int:id>', methods=['GET', 'POST'], name='film')
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


@router('/users')
def users(request):
    return json_render({'users': [
        {
         'id': 4,
          'name': 'harouna'
        },
        {
         'id': 2,
          'name': 'diallo'
        },
    ]})