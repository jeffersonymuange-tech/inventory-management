
from flask import Flask
from crud_routes import crud
from external_routes import external

app = Flask(__name__)
app.register_blueprint(crud)
app.register_blueprint(external)

if __name__ == "__main__":
    app.run(debug=True)
