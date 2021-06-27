from nimba.http import router, render

@router('/')
def home(request):
    return "Nimba Framework installed succesfuly!"


@router('/about')
def about(request):
    return "About form <h1>Nimba</h1>"