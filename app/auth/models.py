from app import db
from werkzeug.security import generate_password_hash, \
                              check_password_hash
import uuid


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(
            db.String(), unique=False,
            index=True, nullable=False)
    username = db.Column(
            db.String(120), nullable=False,
            index=True, unique=True)
    password_hash = db.Column(
            db.String(120), nullable=False, index=True)
    is_admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create(username, password):
        user = User.query.filter_by(username=username).first()
        if not user:
            new_user = User()
            new_user.username = username
            new_user.set_password(password)
            new_user.public_id = str(uuid.uuid4())
            new_user.is_admin = False

            db.session.add(new_user)
            db.session.commit()

            return new_user
        return False


class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(
            db.String(60), nullable=False, index=True)
    last_name = db.Column(
            db.String(60), nullable=False, index=True)
    birth = db.Column(db.String(10), nullable=True, index=True)
    sex = db.Column(db.Boolean, nullable=True)  # True male / False female
    phonenumber = db.Column(db.String(20), nullable=True)
    address = db.Column(
            db.String(200), nullable=True, index=True)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User Info {}>'.format(self.user_id)

    def set_phonenumber(self, phonenumber):
        if phonenumber.isdigit():
            self.phonenumber = phonenumber
            return True
        else:
            return False

    @staticmethod
    def create(user_id, first_name, last_name):
        new_info = UserInfo()
        new_info.user_id = user_id
        new_info.first_name = first_name
        new_info.last_name = last_name
        db.session.add(new_info)
        db.session.commit()
        return new_info
