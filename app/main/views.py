from . import main
from flask import render_template,current_app,request,redirect,url_for,request,current_app,flash
from flask_login import login_required,current_user
from ..models import User, Article,Item
from .forms import ArticleForm
import time 
from .. import db


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    articles = pagination.items
    return render_template('index.html',articles=articles,pagination=pagination)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/publish',methods=['GET', 'POST'])
def publish():
    form=ArticleForm()
    if form.validate_on_submit():
        tag = Item(tag=form.tag.data)
        article=Article(body=form.body.data,title=form.title.data,item=tag)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('publish.html',form=form)

@main.route('/article/<int:id>')
def article(id):
    article=Article.query.get_or_404(id)
    return render_template('article.html', articles=[article])

@main.route('/item/<tag>',methods=['GET','POST'])
def item(tag):
    vector=[]
    items=Item.query.filter_by(tag=tag).all()
    for item in items:
        vector.append(item.articles[0])
    articles=vector
    articles.reverse()
    return render_template('item.html',articles=articles)

@main.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    article=Article.query.get_or_404(id)
    form=ArticleForm()
    if form.validate_on_submit(): 
        article.title=form.title.data
        article.body=form.body.data
        article.item.tag=form.tag.data
        db.session.add(article)
        db.session.commit()
        flash('主人,文章已修改完毕')
        return redirect(url_for('.article',id=article.id))
    form.body.data=article.body
    form.title.data=article.title
    form.tag.data=article.item.tag
    return render_template('edit_article.html',form=form) 


#上下文环境变量定义appname
@main.context_processor
def appinfo():
    return dict(appname=current_app.name)

#上下文环境变量定义current_time() or current_time(%Y-%m-%d)
@main.context_processor
def get_current_time():
    def get_time(timeFormat="%b %d, %Y - %H:%M:%S"):
        return time.strftime(timeFormat)
    return dict(current_time=get_time)

