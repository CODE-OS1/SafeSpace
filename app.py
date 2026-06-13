from flask import Flask, request, jsonify
import pymongo
import os
from dotenv import load_dotenv
import secrets
load_dotenv() # loading environment variables

app = Flask(__name__)

client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
database = client.anonymoustokens
anonymoustokens = database.anonymoustokens
print(client.list_database_names())

# creating anonymous tokens in the database
@app.route("/api/auth/register", methods=["GET", "POST"])
def create_token():
    if request.method == "POST":
        token = secrets.token_urlsafe(10) # a 10 character string for  our token
        anonymoustokens.insert_one({"token": token})
        return jsonify({"token": token}), 201
    return jsonify({"message": "Send a POST request to create a token."}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug = True, host = "0.0.0.0", port = port)