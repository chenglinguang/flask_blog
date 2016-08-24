from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db,login_manager
from datetime import datetime
import bleach
from markdown import markdown


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Article(db.Model):
    __tablename__='articles'
    id=db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title=db.Column(db.String(64),index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    body_html = db.Column(db.Text)

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        #需要转换的标签
        allowed_tags=[
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
            'h1', 'h2', 'h3', 'p', 'img'
        ]
        target.content_html = bleach.linkify(
            bleach.clean(
                markdown(value, output_format='html'),
                tags=allowed_tags,
                strip=True
            )
        )

db.event.listen(Article.body, 'set', Article.on_changed_body)

class Item(db.Model):
    __tablename__='items'
    id=db.Column(db.Integer, primary_key=True)
    tag=db.Column(db.String(64))
    articles = db.relationship('Article', backref='item')

class Like(db.Model):
    __tablename__='likes'
    id=db.Column(db.Integer, primary_key=True)
    like_sum=db.Column(db.Integer)



