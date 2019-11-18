from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config["SECRET_KEY"] = "3d6a60de5e354ce37d2f8ef00f7c7d11"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"


from teamManage import routes
