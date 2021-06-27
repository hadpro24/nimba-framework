from nimba.http import router, render

DEFAULT_DIRECTORY_INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Nimba Framework</title>
  <link rel="icon" href="{{ load_static('nimba/img/nimba.ico') }}" />
  <style type="text/css">
    .contenair {
      width: 70%;
      margin: 20px auto;
      padding: 15px 10px;
      border: 2px solid #E6E6E6;
      border-radius: 10px;
      text-align: center;
      background-color: #fff;
      box-shadow: 10px 5px 5px #EEEEF0;
      font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,Open Sans,Helvetica Neue,sans-serif;;
    }
    img{
      width: 100px;
    }
    body{
      background-color: #F6F6F6;
    }
  </style>
</head>
<body>
  <div class="contenair">
    <h1>Nimba Framework successfully installed</h1>
    <p>Nimba Framework is a modern, fast (coding), web framework with python</p>
    <img src="{{ load_static('nimba/img/nimba-logo.png') }}">
    <p>
      Everything you need to know about Nimba Framework at <a href="https://docs.nimbasolution.com/" target="_blank">https://docs.nimbasolution.com</a>
    </p>
    <hr>
    <p><em>
      Thanks <a href="https://nimbasolution.com" target="_blank">Nimba Solution</a> for Licence
    </em></p>
  </div>
</body>
</html>
"""

@router('/')
def home_default(request):
    return DEFAULT_DIRECTORY_INDEX_TEMPLATE
