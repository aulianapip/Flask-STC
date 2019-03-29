from flask import render_template, request, session, redirect,url_for
from app import app
from openpyxl import load_workbook
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
        find_file = dbmodel.find_file("Judul_Skripsi", "file", file, s)

        if find_file == True:
            dbmodel.delete_same("Judul_Skripsi", "file", file, s)

        dbmodel.insert_file("Judul_Skripsi", "file", file, s)

        get_file = dbmodel.get_file_desc("Judul_Skripsi", "file")
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
        get_sfile = dbmodel.get_file_desc("Judul_Skripsi", "file")
        for w in get_sfile:
            values = w.values()
            for y in values:
                sheet = y

        # get nama file dari database, hasil upload terakhir
        get_nfile = dbmodel.get_file_desc2("Judul_Skripsi", "file")
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
        result_insert_table= dbmodel.insert_cleaning_data("Judul_Skripsi","datanya",data)
        result_insert_header = dbmodel.insert_header("Judul_Skripsi","judulnya",header)
    return render_template('tampil_data.html', tables=[data.to_html(classes='table table-striped table-bordered table-hover')])

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


