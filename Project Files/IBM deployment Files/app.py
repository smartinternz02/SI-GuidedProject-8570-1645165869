# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 17:56:08 2020

@author: Adminr
"""
# importing the necessary dependencies
import numpy as np
from flask import Flask, request, render_template
import pickle
import pandas as pd
import os
import json
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "UsnaFI0JkBWMFbA_AE1VghDZ-7QSlc0XATrW6hrBefp6"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__) # initializing a flask app

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/prediction')
def prediction():
    return render_template('search.html')
@app.route('/predict',methods=['GET','POST'])
def predict():
            #  reading the inputs given by the user
   
    Cement = request.form["Cement"]
    BlastFurnaceSlag = request.form["Blast Furnace Slag"]
    FlyAsh = request.form["Fly Ash"]
    Water = request.form["Water"]
    Superplasticizer = request.form["Superplasticizer"]
    CoarseAggregate = request.form["Coarse Aggregate"]
    FineAggregate = request.form["Fine Aggregate"]
    Age = request.form["Age"]
    t = [[int(Cement),int(BlastFurnaceSlag),int(FlyAsh),int(Water),int(Superplasticizer),int(CoarseAggregate),int(FineAggregate),int(Age)]]
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [['Cement','Blast Furnace Slag','Fly Ash','Water','Superplasticizer','Coarse Aggregate','Fine Aggregate','Age']],"values": t}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/050c3a73-6128-4970-ac50-84873979103b/predictions?version=2022-03-08', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    #predictions = response_scoring.json()
    #pred = response_scoring.json()
    #prediction = pred['predictions'][0]['values'][0][0]
    
   

    

    #print('prediction is', prediction)
    # showing the prediction results in a UI
    return render_template('result.html',prediction_text=response_scoring.json()['predictions'][0]['values'][0][0])

if __name__=="__main__":
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=False)