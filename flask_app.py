from tracemalloc import start
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Lists all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and prcp"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    # Convert list of tuples into normal list
    prcp_dates = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_dates.append(prcp_dict)

    return jsonify(prcp_dates)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and prcp"""
    # Query all passengers
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    station_list = []
    for station in results:
        station_dict = {}
        station_dict["station"] = station
        station_list.append(station_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #Create a session link from Python to the DB
    session = Session(engine)

    """Return the list of the most active station's date and prcp"""
    #Query the results of the most active station
    results = (session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= '2016-08-18').all())
    session.close()

    #Convert list of tuples into a normal list
    date_prcp_list = []
    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["prcp"] = prcp
        date_prcp_list.append(date_prcp_dict)

    return jsonify(date_prcp_list)

@app.route("/api/v1.0/<start>")
def start_date():
    #Create a session link from Python to the DB
    session = Session(engine)
    """Return the list of prcp by start date"""
    #Query the results by input date
    min_results = session.query((func.min(Measurement.tobs)).filter(Measurement.date <= start).all())
    avg_results = session.query((func.avg(Measurement.tobs)).filter(Measurement.date <= start).all())
    max_results = session.query((func.max(Measurement.tobs)).filter(Measurement.date <= start).all())

    session.close()
    #return jsonify of queried results
    return jsonify(min_results,avg_results,max_results)


@app.route("/api/v1.0/<start>/<end>")
def start_end():
    #Create a session link from Python to the DB
    session = Session(engine)
    """Return the dict of queried timeframe data to a list"""
    #Query the results of the input start and end date
    min_results = (session.query(func.min(Measurement.tobs)).\
      filter(Measurement.date >= start).\
      filter(Measurement.date <= end).all())
    avg_results = (session.query(func.min(Measurement.tobs)).\
      filter(Measurement.date >= start).\
      filter(Measurement.date <= end).all())
    max_results = (session.query(func.min(Measurement.tobs)).\
      filter(Measurement.date >= start).\
      filter(Measurement.date <= end).all())
    session.close()
    #Return jsonified results.
    return jsonify(min_results,avg_results,max_results)


if __name__ == '__main__':
    app.run(debug=True)
