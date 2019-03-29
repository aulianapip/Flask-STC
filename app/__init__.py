from flask import Flask

app = Flask(__name__)

from app.module.controller import index
from app.module.controller import Upload
from app.module.controller import Pilih_data
from app.module.controller import Tampil_data