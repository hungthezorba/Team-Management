from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "3d6a60de5e354ce37d2f8ef00f7c7d11"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"


from teamManage import routes
