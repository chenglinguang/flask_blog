from . import main
from flask import render_template,current_app
import time 


@main.route('/')
def index():
    return render_template('index.html')

@main.context_processor
def appinfo():
    return dict(appname=current_app.name)

@main.context_processor
def get_current_time():
    def get_time(timeFormat="%b %d, %Y - %H:%M:%S"):
        return time.strftime(timeFormat)
    return dict(current_time=get_time)


    
