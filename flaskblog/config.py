import os
import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)


class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'mail.privateemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('EMAIL_USER')
    MAIL_PASSWORD = config.get('EMAIL_PASS')
    SITE_WIDTH = 800
    ELASTICSEARCH_URL = config.get('ELASTICSEARCH_URL')
    LANGUAGES = {
        'en': 'English',
        'fr': 'French',
        'de': 'German',
        'es': 'Spanish'
    }
    POSTS_PER_PAGE = 5
    FILES_FOLDER = 'data/'
    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
    UPLOAD_PATH = 'static/uploads'
    ADMIN_USERS = ['nasekins']

