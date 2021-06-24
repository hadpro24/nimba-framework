from framework.nimba.server import Application
import pathlib
from views import *

app = Application(pathlib.Path(__file__).parent.absolute())
app.run()
