from flask import Flask, request, jsonify
from inventory import generate_csv


application = Flask(__name__)

conditions = {
    "nm": "NM-Mint",
    "lp": "Light Play",
    "mp": "Moderate Play",
    "hp": "Heavy Play",
    "dm": "Damaged"
}


@application.route('/csv_from_scryglass', methods=["POST"])
def hello_world():

    success = generate_csv(request.form["from"],
                           conditions.get(request.form["To"].split("@")[0], 'Unknown'),
                           request.form["body-plain"].split('\n'))

    return jsonify({"success": success})


# run the app.
if __name__ == "__main__":
    application.debug = True
    application.run()
