from flask import (
    Flask,
    jsonify, 
    render_template, 
    request,
    abort
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from flask_migrate import Migrate
import uuid
import os

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/dbCPC'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Models
with app.app_context():
   #Convertir el modelo en una tabla
   db.create_all()




# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')




# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))
