from teamManage import db


UserTeam = db.Table(
	"UserTeam",
	db.Column("userId", db.Integer, db.ForeignKey("user.userId")),
	db.Column("teamId", db.Integer, db.ForeignKey("team.teamId"))
)

class User(db.Model):
	userId = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	profile_image = db.Column(db.String(20),nullable=False, default="default.jpg")
	password = db.Column(db.String(60), nullable=False)
	gender = db.Column(db.String(10), nullable=False)
	member = db.relationship("Team", secondary=UserTeam, backref=db.backref("member",lazy="dynamic"))

	def __repr__(self):
		return (f"User ({self.username})")

class Team(db.Model):
	teamId = db.Column(db.Integer, primary_key=True)
	teamName = db.Column(db.String(20),unique=True, nullable=False)
	teamDescription = db.Column(db.Text)

	def __repr__(self):
		return (f"User ({self.teamName})")

