from flask import Flask
import pymongo
import os
from dotenv import load_dotenv

load_dotenv() # loading environment variables


app = Flask(__name__)

client = pymongo.MongoClient(os.getenv("MONGODB_URI")) 
database = client.anonymoustokens 
anonymoustokens = database.anonymoustokens
print(client.list_database_names()) 


















if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug = True, host = "0.0.0.0", port = port)