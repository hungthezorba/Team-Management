from teamManage import db


class User(db.Model):
	id = db.Column(db.integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	profile_image = db.Column(db.String(20), unique=True, default="default.jpg")
	password = db.Column(db.String(60), nullable=False)
	gender = db.Column(db.String(10), nullable=False)

	def __repr__(self):
		return ("User %s %s %s " %(username, email, gender, profile_image))

