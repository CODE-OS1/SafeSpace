from flask import Flask
import pymongo
import os


app = Flask(__name__)

mongodb_uri = "mongodb+srv://sspaceug:E07qMAC82dWok9Dv@cluster0.rcvvqsb.mongodb.net/?appName=Cluster0"
client = pymongo.MongoClient(mongodb_uri) # creating a client using Mongoclient
database = client.anonymoustokens 
anonymoustokens = database.anonymoustokens
print(client.list_database_names()) # test for database connection


















if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug = True, host = "0.0.0.0", port = port)