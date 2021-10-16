from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Create engine
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

#Create table objects
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    print("Request received for 'Home' page...")
    return (
        #img just for some fun
        f'<img src="https://2.bp.blogspot.com/-OdFAI__hKmU/Tbs8iyP6YMI/AAAAAAAABvA/oBjv53PO0Ms/s1600/Hawaii+title.png"><br><br>'
        f"<strong>Hawaii weather API see list below for all routes</strong><br><br>"
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations <br>"
        f"/api/v1.0/tobs <br>"
        f"For the following two use date format YYYY-MM-DD <br>"
        f'/api/v1.0/&ltstart_date&gt <br>'
        f'/api/v1.0/&ltstart_date&gt/&ltend_date&gt')

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Precipitation requested")
    
    #set variables
    most_recent = dt.date(2017, 8, 23)
    query_date = most_recent - dt.timedelta(days=365)
    most_active = "USC00519281"
    
    #pull data
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).order_by(Measurement.date).all()
    session.close()
    
    #format data
    results_list = []
    for date, prcp in results:
        results_dic = {}
        results_dic['date'] = date
        results_dic['prcp'] = prcp
        results_list.append(results_dic)
    
    #return results
    return jsonify(results_list)

@app.route("/api/v1.0/stations")
def stations():
    print("Stations requested")
    
    #pull data
    session = Session(engine)
    results = session.query(Station.station, Station.station).all()
    session.close()
    
    #return results
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Tobs requested")
    
    #set vaiables
    most_recent = dt.date(2017, 8, 23)
    query_date = most_recent - dt.timedelta(days=365)
    most_active = "USC00519281"
    
    #pull data
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_date).filter(Measurement.station == most_active).all()
    session.close()
    
    #return results
    return jsonify(results)


@app.route("/api/v1.0/<start>")
def tobs_start(start):
    print("Tobs start requested")
    
    #pull data
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    
    #format data
    results_list = []
    for min, max, avg in results:
        results_dic = {}
        results_dic['TMIN'] = min
        results_dic['TMAX'] = max
        results_dic['TAVG'] = avg
        results_list.append(results_dic)
    
    #return results
    return jsonify(results_dic)

@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end(start, end):
    print("Tobs start end requested")
    
    #pull data
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    
    #format data
    results_list = []
    for min, max, avg in results:
        results_dic = {}
        results_dic['TMIN'] = min
        results_dic['TMAX'] = max
        results_dic['TAVG'] = avg
        results_list.append(results_dic)
    
    #return results
    return jsonify(results_dic)




if __name__ == "__main__":
    # @TODO: Create your app.run statement here
    app.run(debug=True)
    # YOUR CODE GOES HERE
