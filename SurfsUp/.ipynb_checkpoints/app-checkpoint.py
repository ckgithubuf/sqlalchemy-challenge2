# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
from flask import Flask, jsonify, request


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
    )


@app.route("/api/v1.0/precipitation")
def measurements():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    last_year_data = request.args.get('last_year', None, bool)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    
    session.close()

    results_dict = []
    for date, prcp in results:
        result_dict = {}
        result_dict["date"] = date
        result_dict["prcp"] = prcp
        results_dict.append(result_dict)
    print(len(results_dict))
    return jsonify(results_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Stations).all()
    session.close()

    results_dict = []
    for result in results:
        result_dict = {}
        result_dict["id"] = result.id
        result_dict["station"] = result.station
        result_dict["name"] = result.name
        result_dict["latitude"] = result.latitude
        result_dict["longitude"] = result.longitude
        result_dict["elevation"] = result.elevation
        results_dict.append(result_dict)
    return jsonify(results_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-18').all()
    session.close()

    results_dict = []
    for date, tobs in results:
        result_dict = {}
        result_dict["date"] = date
        result_dict["tobs"] = tobs
        results_dict.append(result_dict)
    print(len(results_dict))
    return jsonify(results_dict)


if __name__ == '__main__':
    app.run(debug=True)