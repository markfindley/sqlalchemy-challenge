import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# 1. Import Flask
from flask import Flask


# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def index():
    # List all routes that are available.
    return (
           f"Here are the available routes:<br/>"
           f"/api/v1.0/precipitation<br/>"
           f"/api/v1.0/stations<br/>"
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/averagetempsbystartdate<br/>"
           f"/api/v1.0/averagetempsbystartandenddate"
    )
    
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation measurements"""
    # Query all measurements
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all status
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["station name"] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)    

# Query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()

    session.close()  

    all_tobs = []
    for station, date, tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)  

# # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/averagetempsbystartdate/<date_string>")
def start(date_string):

    session = Session(engine)

    min_temp = session.query(min(Measurement.tobs)).\
        filter(Measurement.date >= 'date_string').all()

    max_temp = session.query(max(Measurement.tobs)).\
        filter(Measurement.date >= 'date_string').all()

    # avg_temp = session.query(avg(Measurement.tobs)).\
    #     filter(Measurement.date >= 'date_string').all()                

    session.close()      

    return (
           f"Here are the temperatures:<br/>"
           f"The minimum temperature is: {min_temp}<br/>"
           f"The maximumum temperature is: {max_temp}<br/>"
        #    f"The average temperature is: {avg_temp}<br/>"
    )

def to_date(date_string): 
    try:
        return datetime.datetime.strptime(dateString, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(date_string))

@app.route()
def event():
    try:
        ektempo = to_date(request.args.get('start', default = datetime.date.today().isoformat()))
    except ValueError as ex:
        return jsonify({'error': str(ex)}), 400   # jsonify, if this is a json api    
       
# engine.execute('select avg(tobs), min(tobs), max(tobs) from Measurement where date >= "2017-08-23"').fetchall()
# [(80.25, 76.0, 82.0)]       

# # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# @app.route("/api/v1.0/averagetempsbystartandenddate")
# def startandend():

#     return           

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)