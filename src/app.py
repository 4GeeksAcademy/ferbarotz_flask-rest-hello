"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planeta, Personaje
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# -----------INICIO ENDPOINTS----------------------

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#USUARIO

@app.route('/user', methods=['GET'])
def get_users():
    all_user = User.query.all()
    results =list(map(lambda user:user.serialize(),all_user ))

    
   
    return jsonify(results), 200

      
#PLANETA

@app.route('/planeta', methods=['GET'])
def get_planetas():
    all_planetas = Planeta.query.all()
    results =list(map(lambda planeta:planeta.serialize(),all_planetas ))
  
    return jsonify(results), 200

@app.route('/planeta/<int:planeta_id>', methods=['GET'])
def get_planeta(planeta_id):
    planeta= db.session.get(Planeta, planeta_id)

    return jsonify(planeta.serialize()), 200

@app.route('/planeta/<int:planeta_id>', methods=['DELETE'])
def delete_planeta(planeta_id):
    planeta= db.session.get(Planeta, planeta_id)

    response_body = {
        "msg": 'Se elimino el planeta' +  planeta.planeta
    }
    db.session.delete(planeta)
    db.session.commit() 

    return jsonify(response_body), 200


#PERSONAJE

@app.route('/personaje', methods=['GET'])
def get_personajes():
    all_personajes = Personaje.query.all()
    results =list(map(lambda personaje:personaje.serialize(),all_personajes ))
  
    return jsonify(results), 200

@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):
    personaje= db.session.get(Personaje, personaje_id)

    return jsonify(personaje.serialize()), 200

@app.route('/personaje/<int:personaje_id>', methods=['DELETE'])
def delete_personaje(personaje_id):
    personaje= db.session.get(Personaje, personaje_id)

    if personaje is None:
        return {"msg":'No se encontro el planeta'}, 404
           
    response_body = {
        "msg": "Se elimino el personaje"+ personaje.personaje
    }
    db.session.delete(personaje)
    db.session.commit() 

   
    return jsonify(response_body), 200

#PLANETA FAVORITO

@app.route('/planeta', methods=['POST'])
def add_planeta():
    # leer los datos del cuerpo de la solicuitud 
    print(request)
    print(request.get_json())
    #print(request.get_json()["planeta"])
    # agregar a la bd los planetas
    body=request.get_json()

    if 'planeta' not in body:
        return'Debes enviar el planeta'
    
    if body['planeta']=='':
        return 'El planeta no puede estar vacio',400
    
    planeta = Planeta(**body)
    # planeta = Planeta(planeta=body['planeta'],terreno=body['terreno'],poblacion=body['poblacion'])
    # guardar cambios, persistir en la BD
    db.session.add(planeta)
    db.session.commit()
    
    response_body = {
        "msg": "Se creo el planeta",
        "planeta":planeta.serialize()
         
    }

    return jsonify(response_body), 200




#PERSONAJE FAVORITO

@app.route('/personaje', methods=['POST'])
def add_personaje():
    # leer los datos del cuerpo de la solicuitud 
    print(request)
    print(request.get_json())
    #print(request.get_json()["personaje"])
    
    # agregar a la bd los personaje
    body=request.get_json()

    if 'personaje' not in body:
        return'Debes enviar el personaje'
    
    if body['personaje']=='':
        return 'El personaje no puede estar vacio',400

    personaje = Personaje(**body)
    #personaje = Personaje(personaje=body['personaje'],peso=body['peso'],ojos=body['ojos'])
    # guardar cambios, persistir en la BD
    db.session.add(personaje)
    db.session.commit()

    
       
    response_body = {
        "msg": "Se creo el planeta",
        "personaje":personaje.serialize()
         
    }

    return jsonify(response_body), 200
# #prueba
# @app.route('/test/', methods=['GET'])
# def test():

#     response_body = {
#         "msg": "prueba ",
#         "user":{
#            "email":'falso@mail.com'

#        }
#     }

#     return jsonify(response_body), 200

# @app.route('/test/<string:test>', methods=['GET'])
# def test(test):

#     response_body = {
#         "msg": "test ",
#         "user":{
#            "email":'falso@mail.com'

#        }
#     }

#     return jsonify(response_body), 200


# -----------FIN ENDPOINTS----------------------

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
