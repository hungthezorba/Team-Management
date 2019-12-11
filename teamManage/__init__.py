from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
db = SQLAlchemy(app)
# migrate = Migrate(app,db)
# manager = Manager(app)
# manager.add_command('db',MigrateCommand)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config["SECRET_KEY"] = "3d6a60de5e354ce37d2f8ef00f7c7d11"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
socketio = SocketIO(app)

from teamManage import routes
