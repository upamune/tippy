import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask_admin.contrib import sqla
from models import Base, Device

app = Flask(__name__)

# SET YOUR CONFIG
app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 'tippy.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

admin = admin.Admin(app, name='Tippy', url='/', template_mode='bootstrap3')
admin.add_view(sqla.ModelView(Device, db.session))

def build_db():
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)

if __name__ == "__main__":
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_db()
    app.run()


