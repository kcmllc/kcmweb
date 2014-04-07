#SQLALCHEMY_DATABASE_URI = 'mysql://kyle:tolkien1@68.169.60.221/kcmdb'
#SQLALCHEMY_DATABASE_URI = 'mysql://root:anduin@107.170.14.219/kcmdb'
SQLALCHEMY_DATABASE_URI = 'mysql://kyle:anduin@localhost/kcmdb'
SQLALCHEMY_BINDS = {
    'kcmdb': SQLALCHEMY_DATABASE_URI,
    'finintel': 'mysql://kyle:anduin@localhost/financial_intel'
    #'finintel': 'mysql://kyle:tolkien1@68.169.60.221/financial_intel'
}
MONGODB_SETTINGS = {
    'DB': 'fin_intel'
}
MONGOMYADMIN_DATABASES = {
    'local': 'mongodb://localhost:27017'
}
DEBUG = True
SECRET_KEY = 'andtol86'
BOOTSTRAP_SERVE_LOCAL = True
DEBUG_TB_PANELS = {
    'flask.ext.mongoengine.panels.MongoDebugPanel'
}
GOOGLE_DOMAIN = 'knightcapllc.com'
GOOGLE_CONSUMER_KEY='knightcapllc.com'
GOOGLE_CONSUMER_SECRET='97OUK3hTmvC4CDfbFh7rRCb3'
BASE_URL = 'https://www.googleapis.com/oauth2/v1/'
ACCESS_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
AUTHORIZE_URL = 'https://www.google.com/a/knightcapllc.com/o8/ud?be=o8'
CLIENT_ID = '170203394820-pb2mh78h63c23lnpo9rlapdfir0g7g8s.apps.googleusercontent.com'
CLIENT_SECRET = 'fisN_o4Dret19J47R7a83UmU'