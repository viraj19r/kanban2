class LocalDevelopmentConfig():
    # sqlite_db_dir = os.path.join(basedir, "../db_folder")
    SQLALCHEMY_DATABASE_URI = "sqlite:///../db_folder/kanban.sqlite3"
    #  + os.path.join(sqlite_db_dir,"test.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = True #modification will be tracked by flask
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    SECRET_KEY = 'LPNsmCGnNzAzEBImRr0uHFk9XO3CmDLn'
    SECURITY_PASSWORD_SALT	= 'LPNsmCGnNzAzEBImRr0uHFk9XO3CmDLn' #used for double hashing
    SECURITY_PASSWORD_HASH = 'bcrypt' # check whether this stores password after hashing or not
    # SECURITY_REGISTRABLE = True
    # SECURITY_SEND_REGISTER_EMAIL = False
    # SECURITY_UNAUTHORIZED_VIEW = None
    TESTING = True
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
 