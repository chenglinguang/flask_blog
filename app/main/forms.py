from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,HiddenField
from wtforms.validators import Required, Length, Email, Regexp,DataRequired
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import User


class PostForm(Form):
    body = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')

class ArticleForm(Form):
    title = StringField('标题', validators=[Required()])
    body = PageDownField('正文', validators=[Required()])
    #tag  = StringField('标签',validators=[Required()])
    submit = SubmitField('发布文章')



