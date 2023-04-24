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
                                    #Dialect://username:password@host:port/dbname
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alva:123@localhost:5432/test'
app.config['UPLOAD_FOLDER'] = 'static/employees'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Models

    
with app.app_context():
   #Convertir el modelo en una tabla
   db.create_all()

# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))
