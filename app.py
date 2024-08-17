from chalice import Chalice # type: ignore

app = Chalice(app_name='MuscleCore')


@app.route('/')
def index():
    return {'hello': 'world'}

