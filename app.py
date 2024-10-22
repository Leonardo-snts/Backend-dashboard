from flask import Flask
from flask_cors import CORS
from api import api  # Importando o Blueprint 'api' de api/routes.py

app = Flask(__name__)
CORS(app)

# Registrando o Blueprint
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
