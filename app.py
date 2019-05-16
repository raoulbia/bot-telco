#!/usr/bin/env python3
# https://github.com/Ahirice/sato/
# https://cai.tools.sap/blog/python-cryptobot/

from flask import Flask, request, jsonify, render_template
from zipfile import ZipFile
import pandas as pd
import json
import os

app = Flask(__name__)

# app.secret_key = 'your secret'
# app.config['SESSION_TYPE'] = 'filesystem'

port = int(os.environ["PORT"])

zf = ZipFile('local-data/telco-customer-churn.zip')
df = pd.read_csv(zf.open('WA_Fn-UseC_-Telco-Customer-Churn.csv'))
print(df.head())


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html') # use methods = GET


@app.route('/upgrade', methods=['POST'])
def upgrade():
    answer = ''
    upgrade_url = ''
    data = json.loads(request.get_data().decode())
    # print(data)
    # cust_id = data['nlp']['entities']['customer'][0]['raw']
    cust_id = data["conversation"]["memory"]["customer"]["customer_id"]
    row = df[df.customerID==cust_id]
    if len(row) > 0:
        # answer = row.Contract.values[0]
        if row.Contract.values[0] == 'Month-to-month':
            answer = 'Sorry, upgrades are not available for Month-to-month contracts'
            return respond(answer)
        else:
            upgrade_url = 'https://n.vodafone.ie/upgrade-your-phone.html'
            answer = "I checked your account and I'm deligthed to confirm that you are elegible for an upgrade. " \
                     "Click on the link below to find out more!"
            return respond(answer, upgrade_url)

    else:
        answer = 'Sorry, this customer ID is not valid.'
        return respond(answer, validation='no')


@app.route('/contract_query', methods=['POST'])
def contract_query():
    answer = ''
    data = json.loads(request.get_data().decode())
    cust_id = data["conversation"]["memory"]["customer"]["customer_id"]
    row = df[df.customerID == cust_id]
    if len(row) > 0:
        monthly_charges = row.MonthlyCharges.values[0]
        total_charges = row.TotalCharges.values[0]
        answer = 'Your monthly charges are ' + str(monthly_charges) + '£. You have currently spent ' + total_charges + '£.'
        return respond(answer)
    else:
        answer = 'Sorry, this customer ID is not valid.'
        return respond(answer, validation='no')


def respond(answer, upgrade_url=None, validation='yes'):
    return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      # 'content': 'Roger that',
      'content': '%s' % (answer)
    }],
    conversation={
      'memory': { 'url': upgrade_url, 'validation_backend': validation}
    }
)

@app.route('/errors', methods=['POST'])
def errors():
  print(json.loads(request.get_data().decode()))
  return jsonify(status=200)

# if __name__ == "__main__":
#     app.run(debug=True, host = '0.0.0.0', port = 5000)

app.run(port=port, host="0.0.0.0")