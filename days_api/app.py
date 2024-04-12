"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, request, jsonify

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
def between():
    """ Computes how many days between two given dates """
    response = request.json
    for key in ["first", "last"]:
        if key not in response:
            return {"error": "Missing required data."}, 400

    try:
        first = convert_to_datetime(response["first"])
        last = convert_to_datetime(response["last"])
        between = get_days_between(first, last)
        add_to_history(request)
        return {"days": between}, 200
    except:
        return {'error': 'Unable to convert value to datetime.'}, 400


@app.route("/weekday", methods=["POST"])
def weekday():
    """ Returns the day of the week of the date """
    response = request.json

    if 'date' not in response:
        return {"error": "Missing required data."}, 400

    try:
        the_date = convert_to_datetime(response['date'])
        day = get_day_of_week_on(the_date)
        add_to_history(request)
        return {"weekday": day}
    except:
        return {'error': 'Unable to convert value to datetime.'}, 400


@app.route("/history", methods=["GET", "DELETE"])
def history():
    """ Returns history from user's actions """
    if request.method == "GET":
        args = request.args.to_dict()
        number = args.get("number")

        if not number:
            number = 5

        elif not number.isdigit():
            return {"error": "Number must be an integer between 1 and 20."}, 400

        number = int(number)
        if not 1 <= number <= 20:
            return {"error": "Number must be an integer between 1 and 20."}, 400

        add_to_history(request)
        history_of_app = app_history[::-1][:number]
        return jsonify(history_of_app)

    if request.method == "DELETE":
        app_history.clear()
        return {'status': "History cleared"}


@app.route("/current_age", methods=["GET"])
def get_age():
    """ Computes age from user's birthdate """
    args = request.args.to_dict()
    birthdate = args.get("date")

    if not birthdate and not isinstance(birthdate, date):
        return {"error": "Date parameter is required."}, 400

    try:
        age = get_current_age(birthdate)
        add_to_history(request)
        return {"current_age": age}
    except:
        return {"error": "Value for data parameter is invalid."}, 400


if __name__ == "__main__":
    app.run(port=8080, debug=True)
