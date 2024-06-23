from pymongo import MongoClient
from efro.terminal import Clr
import setting

# Load settings from settings.json
settings = setting.get_settings_data()

# Define MongoDB connection details
mongourl = "mongodb+srv://akakak:akakak@cluster0.b6pgq.mongodb.net/?retryWrites=true&w=majority"
new_db_name = 'others'
default_collection_name = 'default'

# Get collection name from settings or use default
database_name = settings["discordbot"].get("database_name", default_collection_name)

try:
    if database_name in ['others', 'default', 'vortex']:
        raise ValueError("Error: Database name cannot be set to 'others' or 'default' in settings.json file. Please change it.")

    print(f'{Clr.CYN}{Clr.BLD}Establishing connection to database..{Clr.RST}')
    mgclient = MongoClient(mongourl)
    new_db = mgclient[database_name]
    Banlist = new_db['bandata']
    dbname = mgclient['vortex']
    playerinfo = dbname['pinfo']
    serverinfo = dbname['serverinfo']
    linkedusers = dbname["linkedusers"]
    notify_list = new_db['notify']
    whitelist = new_db['whitelist']
    complaint_count = new_db['complainter']
    complaints_count = new_db['complaints']
    print(f'{Clr.CYN}{Clr.BLD}Succesfully connected to database!{Clr.RST}')
    print(f'{Clr.CYN}{Clr.BLD}Database Name: {database_name}{Clr.RST}') 
    print(f'{Clr.CYN}{Clr.BLD}Join us on discord : VORTEX AND HONOR PARADISE{Clr.RST}')                                                                                                                
except Exception as err:
    print(f'{Clr.RED}{Clr.BLD}Connection to database failed:\n{err}{Clr.RST}')
    print(f'{Clr.RED}{Clr.BLD}Many features like ban will be non-functioning!')
    raise err  # Raise the error to stop the server if connection fails
