from flask import Flask
from flask_cors import CORS
from controller import routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(routes)
    return app

app = create_app()
app.run()