from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from . import auth
from ..models import User
from .forms import LoginForm
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('无效用户名或密码.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登陆.')
    return redirect(url_for('main.index'))

#@auth.route('/publish')
#@login_required
#def publish():
#    form=ArticleForm()
#    if form.validate_on_submit():
        

