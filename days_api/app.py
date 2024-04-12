"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({"message": "Welcome to the Days API."})


@app.route("/between", methods=["POST"])
def get_between():
    """ Computes how many days between two given dates """
    response = request.json
    try:
        first = convert_to_datetime(response["first"])
        last = convert_to_datetime(response["last"])
        between = get_days_between(first, last)
        print(between)
        add_to_history(request)
        return {"days": between}
    except d:
        return {"error": "Missing required data."}, 400


@app.route("/weekday", methods=["POST"])
def get_weekday():
    """ Returns the day of the week of the date """
    response = request.json
    date = convert_to_datetime(response['date'])
    weekday = get_day_of_week_on(date)
    print(weekday)
    add_to_history(request)
    print(app_history)
    return {"weekday": weekday}


@app.route("/history", methods=["GET", "DELETE"])
def history():
    if request.method == "GET":
        args = request.args.to_dict()
        number = args.get("number")

        if not number or not int(number) or not 1 <= int(number) <= 20:
            number = 5
        else:
            number = int(number)

        add_to_history(request)
        history = app_history[-number:]

        return history

    elif request.method == "DELETE":
        app_history.clear()
        return {'status': "History cleared"}


@app.route("/current_age", methods=["GET"])
def get_age():
    args = request.args.to_dict()
    date = args.get("date")
    dob = convert_to_datetime(date)
    age = get_current_age(dob)
    add_to_history(request)
    return {"current_age": age}


if __name__ == "__main__":
    app.run(port=8080, debug=True)


"""

POST - weekday
http://localhost:8080/weekday

{
    "date": "12.04.2024"
}



GET - history 
http://localhost:8080/history

http://localhost:8080/history?number=2



DELETE - history
http://localhost:8080/history



GET - age
http://localhost:8080/current_age?date=01.07.2002

{
    "date" : "01.07.2002"
}

"""
