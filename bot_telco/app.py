#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template
from zipfile import ZipFile
import pandas as pd
import json
import os
from itertools import compress

app = Flask(__name__, static_url_path='/static')

# reading customer data from file
# zf = ZipFile('data/telco-customer-churn.zip')
# df = pd.read_csv(zf.open('WA_Fn-UseC_-Telco-Customer-Churn.csv'))

# reading data from file containing only demo accounts
df = pd.read_csv('/var/www/html/bot_telco/data/telco-customer.csv')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html') # use methods = GET


@app.route('/upgrade', methods=['POST'])
def upgrade():
    data = json.loads(request.get_data().decode())
    # print(data)
    # cust_id = data['nlp']['entities']['customer'][0]['raw']
    cust_id = data["conversation"]["memory"]["customer"]["customer_id"]
    cust_record = df[df.CustomerID==cust_id]
    print(cust_record)
    if len(cust_record) > 0: # customer record exists

        upgrade = cust_record.Upgrade.values[0]
        churn = cust_record.Churn.values[0]
        ltv = cust_record.LTV.values[0]
        address_home = cust_record.home_address.values[0]
        address_store = cust_record.store_address.values[0]
        # print(upgrade, churn, ltv)
        print(address_store)
        print(address_home)

        offer_reduced = all([upgrade == 'yes', churn == 'yes', ltv == 'high'])
        offer_store_price = any([
                                all([upgrade == 'yes', churn == 'yes', ltv == 'low']),
                                all([upgrade == 'yes', churn == 'no'])
                                ])
        offer_none = all([upgrade == 'no'])
        print(offer_reduced, offer_store_price, offer_none)

        offer_reduced_text = "I checked your account and I'm deligthed to confirm that you are elegible for an upgrade " \
                             "at a REDUCED PRICE! :) "

        offer_store_price_text = "I checked your account and I'm deligthed to confirm that you are elegible for an upgrade."

        offer_none_text = "Sorry, upgrades are not available for Pay as You Go customers.   "

        text = [offer_reduced_text, offer_store_price_text, offer_none_text]
        filter = [offer_reduced, offer_store_price, offer_none]

        answer = list(compress(text, filter))[0]
        print(answer)

        offer = 'store_price'
        if offer_reduced:
            offer = 'reduced_price'
        if offer_none:
            offer = None
        print('oofer', offer)
        return respond(answer, offer, str(address_home), str(address_store))

    else:
        answer = 'Sorry, this customer ID is not valid.'
        address_home = None
        address_store = None
        offer=None
        return respond(answer, offer, address_home, address_store, validation='no')


# @app.route('/contract_query', methods=['POST'])
# def contract_query():
#     answer = ''
#     data = json.loads(request.get_data().decode())
#     cust_id = data["conversation"]["memory"]["customer"]["customer_id"]
#     row = df[df.customerID == cust_id]
#     if len(row) > 0:
#         monthly_charges = row.MonthlyCharges.values[0]
#         total_charges = row.TotalCharges.values[0]
#         answer = 'Your monthly charges are ' + str(monthly_charges) + '£. You have currently spent ' + total_charges + '£.'
#         return respond(answer)
#     else:
#         answer = 'Sorry, this customer ID is not valid.'
#         return respond(answer, validation='no')


def respond(answer, offer, home_address=None, store_address=None, validation='yes'):
    return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      # 'content': 'Roger that',
      'content': '%s' % (answer)
    }],
    conversation={
      'memory': { 'offer_type': offer,
                  'validation_backend': validation,
                  'home_addr': home_address,
                  'store_addr': store_address}
    }
)

@app.route('/errors', methods=['POST'])
def errors():
  print(json.loads(request.get_data().decode()))
  return jsonify(status=200)


if __name__ == "__main__":

    # local testing
    # app.run(debug=True, host = '0.0.0.0', port = 5000)

    # for Heroku deployment
    port = int(os.environ['PORT'])
    print(port)
    app.run(debug=True, port=port, host="0.0.0.0")
