from teamManage import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

UserTeam = db.Table(
	"UserTeam",
	db.Column("userId", db.Integer, db.ForeignKey("user.id")),
	db.Column("teamId", db.Integer, db.ForeignKey("team.id")), 
	db.PrimaryKeyConstraint('userId', 'teamId')
)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	profile_image = db.Column(db.String(20),nullable=False, default="default.jpg")
	password = db.Column(db.String(60), nullable=False)
	gender = db.Column(db.String(8), nullable=False)
	member = db.relationship("Team", cascade="all", secondary=UserTeam,backref=db.backref("members",lazy="dynamic"))
	phoneNumber = db.Column(db.String, unique=True, nullable=True)
	biography = db.Column(db.String, unique=False, nullable=True)

	def __repr__(self):
		return (f" ({self.username}, {self.email}, {self.gender}, {self.phoneNumber}, {self.member})")

class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20),unique=True, nullable=False)
	description = db.Column(db.Text)
	tasks = db.relationship("Task", backref="inTeam", lazy=True) 

	def __repr__(self):
		return (f" ({self.name}, {self.description}, {self.tasks})")

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.Text, nullable=False)
	status = db.Column(db.Boolean, nullable=False, default=False)
	team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)

	def __repr__(self):
		return (f" ({self.name}, {self.description}, {self.status}, {self.team_id})")

#class Post(db.Model)