from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager

mongo = PyMongo()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/hospital_db'

    mongo.init_app(app)
    login_manager.init_app(app)

    from .routes import auth, patient, doctor, admin, home
    app.register_blueprint(auth.bp)
    app.register_blueprint(patient.bp)
    app.register_blueprint(doctor.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(home.bp)

    return app 
