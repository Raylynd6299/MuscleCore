from chalice import Chalice # type: ignore

from chalicelib.db import init_db 

app = Chalice(app_name='MuscleCore')
app.debug = True
app.api.cors = True

init_db()

@app.route('/')
def index():
    return {'hello': 'world'}

