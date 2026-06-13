from flask import Flask, request, jsonify
import pymongo
import os
from dotenv import load_dotenv
import secrets
from datetime import datetime



load_dotenv() # loading environment variables

app = Flask(__name__)

client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
database = client.anonymoustokens
anonymoustokens = database.anonymoustokens
print(client.list_database_names())

# creating anonymous tokens in the database
@app.route("/anontoken", methods=["GET", "POST"])
def create_token():
    if request.method == "POST":
        token = secrets.token_urlsafe(10) # a 10 character string for  our token usable by the user anytime at login
        anonymoustokens.insert_one({
            "token": token,
            "current_name": generate_anon_name,
            "name_history": [],
            "flag_count": 0,
            "is_banned": False,
            "created_at": datetime.utcnow(),
            "last_seen": datetime.utcnow
        })
        
        return jsonify({"token": token}), 201
    return jsonify({"message": "Send a POST request to create a token."}), 200


"""When a user logs in, they are assigned a anonymous username and a token.
They use this toke to login anytime they want to login and it is by tjis token
we know their identity on the app"""

@app.route("/session/<token>")
def session_login(token):
    user = database.find_one({"token": token})

    if not user:
        return jsonify ({"error": "Invalid Token"}), 401
    
    if user["is_banned"]:
        return jsonify({"error": "Account suspended"}), 403
    
    new_name = generate_anon_name()

    database.users.update_one(
        {
            "_id": user["_id"]
        },
        {
            "$set": {
                "current_name": new_name,
                "last_seen": datetime.utcnow()
            },
            "$push": {"name_history": new_name}
        }
    )
    return jsonify (
        {
            "message": "Welcome",
            "your_name_today": new_name
        }
    )
    


# function that generates an anonymous name for the user
def generate_anon_name ():
    adjectives = ["Kronkron", "Tumi", "Fitaa", "D)fo", "Adamfo", "Boafo", "Obiremp)n", "Ahoto"]
    nouns  = ["Okra", "Nk)sua", "Osrane", "Owia","Esono", ")soro", "Epo", "Patuo"]
    import random
    return f"Anon-{random.choice(adjectives)}{random.choce(nouns)}"




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug = True, host = "0.0.0.0", port = port)