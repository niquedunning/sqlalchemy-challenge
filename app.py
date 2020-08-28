import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measure = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def home():
    print("Server recieved request for my 'Home' page")
    return (
        f"Available Routes for precipitation data in Hawaii API:<br/>"
        f"print precipitation numbers-- "
        f"/api/v1.0/precipitation<br/>"
        f"print list of stations-- "
        f"/api/v1.0/stations<br/>"
        f"print daily temperatures for station Waihee, the station with the most observations-- "
        f"/api/v1.0/tobs<br/>"
        f"print the maximum temp, minimum temp, and average temp starting from a given date-- "
        f"/api/v1.0/2016-09-15<br/>"
        f"print the maximum temp, minimum temp, and average temp</br> "
        f"from a starting date to an end date-- "
        f"/api/v1.0/2016-09-15/2017-08-18"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return a list of all stations"""
    results = session.query(measure.date, measure.prcp).all()

    session.close()

    precip = list(np.ravel(results))

    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Return a list of all stations"""
    results = session.query(station.station, station.name).all()

    session.close()

    stat = list(np.ravel(results))

    return jsonify(stat)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Return a list of all stations"""
    query_result = session.query(measure.date, measure.tobs).\
    filter(measure.station == 'USC00519281').\
    filter(measure.date >= '2016-08-23').all()

    session.close()

    temps = list(np.ravel(query_result))


    return jsonify(temps)


@app.route("/api/v1.0/<start>")
def start(start):
    
    session = Session(engine)

    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')

    sel = [func.round(func.avg(measure.tobs)), 
       func.round(func.max(measure.tobs)), 
       func.round(func.min(measure.tobs))]
    
    session.close()
   
    measures = session.query(*sel).\
    filter(func.strftime("%Y-%m-%d", measure.date) >= start_dt).all()


    results = list(np.ravel(measures))

    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    end_dt = dt.datetime.strptime(end, '%Y-%m-%d')

    sel = [func.round(func.avg(measure.tobs)), 
       func.round(func.max(measure.tobs)), 
       func.round(func.min(measure.tobs))]
    
    session.close()
   
    measures = session.query(*sel).\
    filter(func.strftime("%Y-%m-%d", measure.date) >= start_dt).\
    filter(func.strftime("%Y-%m-%d", measure.date) <= end_dt).all()

    results = list(np.ravel(measures))

    return jsonify(results) 

if __name__ == "__main__":
    app.run(debug=True)