from flask import Flask
from flask_cors import CORS
from controller import routes
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(routes)
    return app

app = create_app()
port = int(os.environ.get("PORT", 5000))
app.run()