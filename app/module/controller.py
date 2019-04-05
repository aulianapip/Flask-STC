from flask import render_template, request, session, redirect,url_for
from app import app
from openpyxl import load_workbook
import pandas as pd
import os

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
# remover = StopWordRemoverFactory().create_stop_word_remover()
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
stemmer = StemmerFactory().create_stemmer()

@app.route('/index')
def index():
    
    return render_template('index.html')

# @app.route('/admin')
# def login():
#     return render_template("login.html")

# @app.errorhandler(404)
# def notfound(error):
#     return render_template("404.html")


@app.route('/upload')
def Upload():
    return render_template('upload.html')

@app.route('/tampil_data', methods= ['GET','POST'])
def Tampil_data():
    if request.method == 'POST':

        select1 = 1
        select2 = 10
        selectcolom ="4"
        namacolom = "judul"

        wb = load_workbook(filename='app/upload_data/penelitian.xlsx')
        sheet_ranges = wb['DANA UAD']
        data = pd.DataFrame(sheet_ranges.values)

        row1 = int(select1)
        row2 = int(select2)

        cols = selectcolom.split(",") #memisahkan inputan kolom dipilih berdasarkan koma
        cols = list(map(int,cols)) #corvert to int
        xname = namacolom.split(",") #memisahkan inptan nama kolom berdasarkan koma
        data =data[row1:row2][cols]#data terpilih berdasarkan inputan baris dan kolom
        data.columns = [xname]

# -----------stopword-------------------------------
        factory = StopWordRemoverFactory()
        stopword = factory.create_stop_word_remover()

        a = []
        a.append(data['judul'].values.tolist())
        
        list_sentence=[]
        for reviews in a:
            for review in reviews:
                data_clean = review.lower()
                list_sentence.append(stopword.remove(data_clean))
# -----------end of stopword-----------------------

# -----------steming-------------------------------
        list_stem = []
        for reviews in list_sentence:
                data_stem = (reviews.encode("ascii","ignore"))
                list_stem.append(stemmer.stem(data_stem))
# -----------end of steming------------------------
        

        pd.options.display.max_colwidth = 999
        data = pd.DataFrame(list_stem)
        head_filter = []
        for index in data.columns:
            custom_head = "Judul" 
            head_filter.append(custom_head)
        data.columns = head_filter

    return render_template('tampil_data.html', tables=[data.to_html(classes='table table-striped table-bordered table-hover')])


@app.route('/stc', methods= ['GET','POST'])
def stc():
    return render_template("stc.html")

@app.route('/hasil_cluster', methods= ['GET','POST'])
def hasil_cluster():
    return render_template("hasil_cluster.html")


