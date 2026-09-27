from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
db_user= os.environ["DB_USER"]
db_password= os.environ["DB_PASSWORD"]
db_host= os.environ["DB_HOST"]
db_port= os.environ["DB_PORT"]
db_name= os.environ["DB_NAME"]
db_sslmode= os.environ["DB_SSLMODE"]

db_url= f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode={db_sslmode}"