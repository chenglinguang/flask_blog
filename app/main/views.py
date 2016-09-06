import os
from werkzeug import secure_filename
from . import main
from flask import render_template,current_app,request,redirect,url_for,request,current_app,flash
from flask_login import login_required,current_user
from ..models import User, Article,Item
from .forms import ArticleForm,UploadForm
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

# 设置允许上传的文件类型
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg'])
UPLOAD_FOLDER = './uploads'
#检查文件类型是否合法
def allowed_file(filename):
    # 判断文件的扩展名是否在配置项ALLOWED_EXTENSIONS中
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def GetFileList(dir,fileList):
    newDir=dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList

@main.route('/upload',methods=['GET','POST'])
def upload():
    form=UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        if filename and allowed_file(filename):
            form.file.data.save('uploads/'+filename)
            return "上传成功"
        else:
            return "上传失败"
    else:
        filelist=GetFileList('uploads/', [])
        return render_template('upload.html',form=form,filelist=filelist)
    
@main.route('/delete/<int:id>',methods=['GET','POST'])
def delete(id):
    article=Article.query.get_or_404(id)   
    db.session.delete(article)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('.index'))

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

