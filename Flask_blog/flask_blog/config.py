import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # getting email from my environment varible
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # getting email-password from my environment varible
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    print(MAIL_PASSWORD)
    # emapiafogiokdkgs