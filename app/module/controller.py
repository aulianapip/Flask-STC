from flask import render_template, request
from app import app

@app.route('/')
def index():
    pageData = {
        "breadcrumb": "Dashboard",
        "pageHeader": "Dashboard",
        "pages": "dashboard.html"
    }
    return render_template("index.html", pageData=pageData)

# @app.route('/admin')
# def login():
#     return render_template("login.html")

@app.errorhandler(404)
def notfound(error):
    return render_template("404.html")


@app.route('/upload', methods= ['GET','POST'])
def upload():
    return render_template("upload.html")

@app.route('/pilih_data', methods= ['GET','POST'])
def pilih_data():
    return render_template("pilih_data.html")

@app.route('/tampil_data', methods= ['GET','POST'])
def tampil_data():
    return render_template("tampil_data.html")

@app.route('/stopword', methods= ['GET','POST'])
def stopword():
    return render_template("stopword.html")

@app.route('/stemming', methods= ['GET','POST'])
def stemming():
    return render_template("stemming.html")

@app.route('/stc', methods= ['GET','POST'])
def stc():
    return render_template("stc.html")

@app.route('/hasil_cluster', methods= ['GET','POST'])
def hasil_cluster():
    return render_template("hasil_cluster.html")


