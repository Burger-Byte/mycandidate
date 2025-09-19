from main.app import db
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
from main.database.models.config import Config
from main.database.models.candidates import get_data
