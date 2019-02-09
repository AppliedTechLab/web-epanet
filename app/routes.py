from app import app
from flask import render_template
from app.forms import UploadForm

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html', title='Home')


@app.route('/upload')
def upload():
    #form = UploadForm()
    return render_template('upload.html', title='Upload')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
