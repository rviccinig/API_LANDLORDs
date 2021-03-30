
# This is the basic executable file
import os
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate


# Create the Flask APP
app=Flask(__name__)
api=Api(app)

###################################################
################ CONFIGURATIONS ###################
##################################################

# Often people will also separate these into a separate config.py file
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


##################################################
################ DATABASE #######################
##################################################

db = SQLAlchemy(app)
Migrate(app,db)
api = Api(app)


#################################################
############# Security & Authentication ########
################################################

from werkzeug.security import safe_str_cmp

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)

from flask_jwt import JWT ,jwt_required

# this creates a new endpoint /auth we have to test it in postman and get the token
# Just send back user and password and it gives me back a token on postman
# Once I have this token I can put on authorization request to see the list in the headers
# JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTcxMTg0OTgsImlhdCI6MTYxNzExODE5OCwibmJmIjoxNjE3MTE4MTk4LCJpZGVudGl0eSI6NH0.1otND4_T4v49QRYahWgGowlz9MOOsh598tqPlyy2c_g
jwt = JWT(app, authenticate, identity)


####################################################
############### Model ###################3
##################################################3

#Aqui estoy creando las tablas dentro de la base de datos de la aplicacion.
# Voy importando la base de datos del archivo donde cree db

# SQLAlchemy me permite heredar facilmente ciertas propiedades de db.MODELS
# En la clase usuario usando werkzeug creo un hash para esto
class User(db.Model):
    __tablename__='user_table'
    __table_args__ = {'extend_existing': True}

    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True)
    username=db.Column(db.String(64),unique=True)
    password=db.Column(db.String(128))

    def __init__(self,email,username,password):
        self.email=email
        self.username=username
        self.password=password

    #This method saves teh user in the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return f"id:{self.id},email: {self.email},username:{self.username},password: {self.password}"

    # Instead of calling 'User' I use the decorator @classmethod, I can use this method without starting an instal of USER!
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()


##################################################
################ RESOURCES #######################
##################################################

from flask_restful import Resource, reqparse

#Resource to register a new '/register'
class register_user(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = register_user.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = User(data['email'],data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

## Resource to see all registered users
class UserList(Resource):
    @jwt_required()
    def get(self):
        result=User.query.all()
        users_list=[]
        content={}
        return {'items': list(map(lambda x: str(x), result))}

####################################################################
#####################End End Points ################################
####################################################################

api.add_resource(register_user,'/register')
api.add_resource(UserList,'/see_all')

#Running the Application
if __name__ == '__main__':
    app.run(debug=True)
