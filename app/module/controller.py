from flask import render_template, request, session, redirect,url_for
from app import app
from openpyxl import load_workbook
import pandas as pd
import os
import dbmodel as x
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

@app.route('/pilih_data', methods= ['GET','POST'])
def Pilih_data():
    

    if request.method == 'POST':
        f = request.files['file']
        file = f.filename
        s = request.form['sheet']
        f.save(os.path.join('app/upload_data', file))

        dbmodel = x.DBModel()
        find_file = dbmodel.find_file("Judul_Penelitian", "file", file, s)

        if find_file == True:
            dbmodel.delete_same("Judul_Penelitian", "file", file, s)

        dbmodel.insert_file("Judul_Penelitian", "file", file, s)

        get_file = dbmodel.get_file_desc("Judul_Penelitian", "file")
        for w in get_file:
            values = w.values()
            for y in values:
                y = y

        wb = load_workbook(filename="app/upload_data/"+file)
        for u in wb.get_sheet_names():
            if u == y:
                sheet_available = True
                break
            else:
                sheet_available = False

        if sheet_available == False:
            return render_template("upload_data.html")

        sheet_ranges = wb[request.form['sheet']]
        data = pd.DataFrame(sheet_ranges.values)
    return render_template('pilih_data.html', tables=[data.to_html(classes='table table-striped table-bordered table-hover')])

@app.route('/tampil_data', methods= ['GET','POST'])
def Tampil_data():
    if request.method == 'POST':

        select1 = request.form["select1"]
        select2 = request.form["select2"]
        selectcolom =request.form["selectcolom"]
        namacolom = request.form["namacolom"]

        dbmodel = x.DBModel()
        # get sheet dari database, hasil upload terakhir
        get_sfile = dbmodel.get_file_desc("Judul_Penelitian", "file")
        for w in get_sfile:
            values = w.values()
            for y in values:
                sheet = y

        # get nama file dari database, hasil upload terakhir
        get_nfile = dbmodel.get_file_desc2("Judul_Penelitian", "file")
        for n in get_nfile:
            values = n.values()
            for q in values:
                file = q

        wb = load_workbook(filename='app/upload_data/'+file)
        sheet_ranges = wb[sheet]
        data = pd.DataFrame(sheet_ranges.values)

        row1 = int(select1)
        row2 = int(select2)

        cols = selectcolom.split(",") #memisahkan inputan kolom dipilih berdasarkan koma
        cols = list(map(int,cols)) #corvert to int
        xname = namacolom.split(",") #memisahkan inptan nama kolom berdasarkan koma
        data =data[row1:row2][cols]#data terpilih berdasarkan inputan baris dan kolom
        data.columns = [xname]
        data = data.dropna()

        header = {}
        for index, head in enumerate(xname):
            header[str(index)] = head

        pd.options.display.max_colwidth = 999

        dbmodel = x.DBModel() #memanggil file model dimodel class DBModel
        result_insert_table= dbmodel.insert_cleaning_data("Judul_Penelitian","datanya",data)
        result_insert_header = dbmodel.insert_header("Judul_Penelitian","judulnya",header)
    return render_template('tampil_data.html', tables=[data.to_html(classes='table table-striped table-bordered table-hover')])

@app.route('/stopword', methods= ['GET','POST'])
def stopword():

    dbmodel = x.DBModel()
    get_data = dbmodel.get_data_all("Judul_Penelitian", "datanya")
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()

    # list_sentence = []
    # for reviews in get_data:
    # 	for review in reviews:
    # 		data_clean = review.lower()
    # 		isi = data_clean.values()
    # 	# isi_judul = isi
    # 	# data_clean = isi.lower()
    # 		list_sentence.append(stopword.remove(data_clean))
    
    data_s=[]
    for i in get_data :
		isi = i.values()
		isi_judul = isi[0]
		data_baru2 = isi_judul.lower()
		data_s.append(stopword.remove(data_baru2))



    data = pd.DataFrame(data_s)
    head_filter = []
    for index in data.columns:
        custom_head = "K" + str(index)
        head_filter.append(custom_head)
    data.columns = head_filter

    dbmodel = x.DBModel()  # memanggil file model dimodel class DBModel
    dbmodel.insert_filtering("Judul_Penelitian", "Stopword", data)
    

    return render_template('stopword.html', tables=[data.to_html(classes='table table-striped table-bordered table-hover')])

@app.route('/stemming', methods= ['GET','POST'])
def stemming():
    return render_template("stemming.html")

@app.route('/stc', methods= ['GET','POST'])
def stc():
    return render_template("stc.html")

@app.route('/hasil_cluster', methods= ['GET','POST'])
def hasil_cluster():
    return render_template("hasil_cluster.html")


