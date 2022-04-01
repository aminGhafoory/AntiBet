from fastapi import FastAPI
import configparser
from database import *


# +----------------------------------
config = configparser.ConfigParser()
config.read("config.ini")

data_base_name = config["db"]["data_base_name"]
blacklist_table_name = config["db"]["blacklist_table_name"]
links_table_name = config["db"]["links_table_name"]
blacklist_file = config["db"]["blacklist_file"]
# +--------------------------------------


conn = create_connection(data_base_name)
c = conn.cursor()


app = FastAPI(
    title="AntiBet",
    version="1.0.0",
    openapi_url=None,
)


@app.get("/links")
async def get_links():
    return show_all_links_db_api(conn=conn, table_name=links_table_name)
