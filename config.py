import os

from dotenv.main import load_dotenv

load_dotenv()

PG_HOST = os.environ['PG_HOST']
PG_PORT = os.environ['PG_PORT']
PG_USER = os.environ['PG_USER']
PG_PASS = os.environ['PG_PASS']
PG_DB = os.environ['PG_DB']

PG_CONF = {
    'host': PG_HOST,
    'port': PG_PORT,
    'username': PG_USER,
    'password': PG_PASS,
    'database': PG_DB,
}

