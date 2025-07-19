import os
from flask_admin import Admin
from models import db, User, Planeta, Personaje,Planetafav,Personajefav,Videojuego
from flask_admin.contrib.sqla import ModelView

class PlanetafavAdmin(ModelView):
    column_list = ('id', 'user_id', 'planeta_id')
    form_columns = ('user', 'planeta')

class PersonajefavAdmin(ModelView):
    column_list = ('id', 'user_id', 'personaje_id')
    form_columns = ('user', 'personaje')

class VideojuegoAdmin(ModelView):
    colums_list =("id","nombre","genero","year","empresa")
    form_colums =("nombre","genero","year","empresa")



def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    
    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Planeta, db.session))
    admin.add_view(ModelView(Personaje, db.session))
    admin.add_view(PlanetafavAdmin(Planetafav, db.session))
    admin.add_view(PersonajefavAdmin(Personajefav, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))