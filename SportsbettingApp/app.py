# import necessary libraries
from models import create_classes
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Pet = create_classes(db)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["petName"]
        lat = request.form["petLat"]
        lon = request.form["petLon"]

        pet = Pet(name=name, lat=lat, lon=lon)
        db.session.add(pet)
        db.session.commit()
        return redirect("/", code=302)

    return render_template("form.html")


@app.route("/api/pals")
def pals():
    results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()

    hover_text = [result[0] for result in results]
    lat = [result[1] for result in results]
    lon = [result[2] for result in results]

    pet_data = [{
        "type": "scattergeo",
        "locationmode": "USA-states",
        "lat": lat,
        "lon": lon,
        "text": hover_text,
        "hoverinfo": "text",
        "marker": {
            "size": 50,
            "line": {
                "color": "rgb(8,8,8)",
                "width": 1
            },
        }
    }]

    return jsonify(pet_data)

@app.route("/api/NFLRoute")
#returns data of all odds from a requested team jsonified
def NFLRoute(TeamName):
    #creates a tuple of NFL records of the team name requested
    TeamData = db.session.query(NFL_Opening_Odds2).filter(Home_Team == TeamName or Away_Team == TeamName).all()
    
    TeamOutput = []
    #loop through values in NFLData and put it in correct format jsonify
    for item in TeamData:
        output = {
            "Date":item[1],
            "Home Team":item[2],
            "Away Team":item[3],
            "Home Win?":item[4],
            "Home Odds":item[5],
            "Away Odds":item[6]
        }
        TeamOutput.append(output)

    return jsonify(TeamOutput)

@app.route("/api/HorseRoute")
#returns horse betting jsonified data
def HorseRoute():
    HorseData = db.session.query(tips2).all()

    HorseOutput = []

    for item in HorseData:
        output ={
            "Date":item[3],
            "Track":item[4],
            "Horse":item[5],
            "Bet Type":item[6],
            "Odds":item[7],
            "Result":item[8]
        }
        HorseOutput.append(output)
     
    return jsonify(HorseOutput)

@app.route("api/UFCRoute")
#returns UFC fight data jsonified
def UFCRoute():
    UFCData = db.session.query(ufcfinal_df2).all()

    UFCOutput = []

    for item in UFCData:
        output ={
            "Red Corner Fighter 1":item[1],
            "Blue Corner Fighter 1":item[2],
            "Red Fighter 1 Odds":item[3],
            "Blue Fighter 1 Odds":item[4],
            "Winner of Fight 1":item[5],
            "Red Corner Fighter 2":item[6],
            "Blue Corner Fighter 2":item[7],
            "Red Fighter 2 Odds":item[8],
            "Blue Fighter 2 Odds":item[9],
            "Winner of Figth 2":item[10]
        }
        UFCOutput.append(output)
     
    return jsonify(UFCOutput)

if __name__ == "__main__":
    app.run()
