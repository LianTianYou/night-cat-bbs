import datetime

JSON_AS_ASCII = False
SECRET_KEY = "ESpNBzBeFe6qQWfx2GKCupQhPQ09WB1f"

# jwt
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
JWT_SECRET_KEY = 'super-secret'

# mysql
host = "47.120.40.123"
port = 3306
user = "root"
password = "rootroot"
database = "night_cat_bbs"

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8"