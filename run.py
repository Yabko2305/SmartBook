from app import app
from app import app, db
from app.models import User, Reservation, Classroom

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Reservation': Reservation, 'Classroom': Classroom}