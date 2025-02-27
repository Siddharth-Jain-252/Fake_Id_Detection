from flask import Flask, request, jsonify ,render_template
from flask_cors import CORS
import instaloader
import pandas as pd
import pickle

app = Flask(__name__)
CORS(app,resources={r"/get_details": {"origins": "*"}})  # Enable Cross-Origin Requests (needed for JavaScript fetch)

# Load ML model

with open('model.pkl', 'rb') as file:
    model2 = pickle.load(file)

# Function to check if an account is fake
def check_fake(username):
    try:
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, username)

        Username = profile.username
        Bio = profile.biography
        Pfp = bool(profile.profile_pic_url)
        Followers = profile.followers
        Following = profile.followees
        Number_of_Posts = profile.mediacount
        Private = int(profile.is_private)
        Full_Name = profile.full_name
        External_URL = int(profile.external_url is not None)

        discription = len(Bio.split())
        fullname_words = len(Full_Name.split())

        c1 = sum(1 for i in Username if i.isdigit())
        c2 = sum(1 for i in Full_Name if i.isdigit())

        df = {
            "profile pic": [int(Pfp)],
            "nums/length username": [c1 / len(Username) if len(Username) > 0 else 0],
            "fullname words": [fullname_words],
            "nums/length fullname": [c2 / len(Full_Name) if len(Full_Name) > 0 else 0],
            "description length": [discription],
            "external URL": [External_URL],
            "private": [Private],
            "#posts": [Number_of_Posts],
            "#followers": [Followers],
            "#follows": [Following]
        }

        main_df = pd.DataFrame(df)
        pred = model2.predict(main_df)

        return {"username": username, "fake": bool(pred[0])}
    except Exception as e:
        return {"error": "Invalid username or profile not found"}

@app.route('/')
def home():
    return render_template('index.html')

# API Route
@app.route("/get_details", methods=["GET"])
def get_details():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    result = check_fake(username)
    return jsonify(result)

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)
