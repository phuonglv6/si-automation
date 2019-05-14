import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    BASE_DIR=basedir
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'
    UPLOAD_FOLDER = os.path.join(basedir,'webapp','static','media')
    OUT_EXTRACTION_FOLDER = os.path.join(UPLOAD_FOLDER,'out_extraction')
    ALLOWED_EXTENSIONS = set(['docx', 'pdf', 'xlsx', 'xls', 'doc'])
    CHARATERS_SPLIT_MARK = ['/', '|', '*', '\n', ':', ' ']
    CONTRAINER_WEIGHT = ['KGS', 'KG']
    CONTRAINER_CBM = ['CBM']
    CONTRAINER_TYPES = ['HC', 'GP', 'G0', 'HR',
                        'G1', 'PF', 'P1', 'HP', 'DC', 'HQ', 'RF']
    CONTAINER_PACKAGE_UNITS = [
        'CARTON',
        'CTN',
        'ctn',
        'PACKAGE',
        'PKG',
        'PALLET',
        'PLT',
        'ROLL',
        'CASE',
        'BOBBIN',
        'PIECE',
        'BAG'
    ]
    DECIMA_SPLIT = ','



class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    POSTGRES_URL="127.0.0.1:5432"
    POSTGRES_USER="phuonglv"
    POSTGRES_PW="123789"
    POSTGRES_DB="si_dounet"
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

