import os


class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ece1779-a2-secretkey'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/testtable'
    #os.environ.get('DATABASE_URL') or \
                              #//'mysql://ece1779database:ece1779database@ece1779database.cpt3hodccygr.us-east-1.rds.amazonaws.com/testtable'
    MAIL_SERVER = 'smtp.googlemail.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    #need valid google map api key to work
    GOOGLEMAPS_KEY = "dummy_key"
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
