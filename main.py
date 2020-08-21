#!/usr/bin/env python
from defines import main
from flask import Flask, url_for, render_template, send_from_directory, request, json, jsonify, Response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def edit():
    country = request.args.get("country", 0)
    if country == 0 :
        response = {"ERROR":"TYPE COUNTRY","TIPS":"https://covid.bksn.se/?country=usa"}
        return Response(str(response), mimetype='application/json')
    response = main(country)
    return Response(str(response), mimetype='application/json')

# WEBHOOK SLACK
@app.route('/slack/country', methods=['POST'])
def slash():
    command_text = request.form
    # print(command_text)
    country = request.form.getlist('text')[0]
    response = main(country)
    payload = {"attachments": [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#E01E5A",
            'text': ':bucksense:* COVID* :rotating_light:\n'+str(response)

        }
    ]
    }
    return jsonify(payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=22115, debug=True)