from flask import Flask, request, jsonify
from inventory import generate_csv


application = Flask(__name__)

conditions = {
    "nm": "Mint/NM",
    "lp": "Lightly Play",
    "mp": "Moderate Play"
}


@application.route('/csv_from_scryglass', methods=["POST"])
def hello_world():

    success = generate_csv(request.form["from"],
                           conditions.get(request.form["To"].split("@")[1], 'Unknown'),
                           request.form["body-plain"].split('\n'))

    return jsonify({"success": success})


# run the app.
if __name__ == "__main__":
    application.debug = True
    application.run()
