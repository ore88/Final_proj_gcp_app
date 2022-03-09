import os
import pandas as pd
import numpy as np
from flask import Flask,request, url_for, redirect, render_template, jsonify
import pickle
from google.cloud import storage
from pycaret.regression import *

app = Flask(__name__)

# Loading the model for predictions
model= load_model('/home/mmaajjuulloo/Final_proj_gcp_app/tuned_knn_gcp')

cols = ['battery_power','blue','clock_speed','dual_sim','fc','four_g','int_memory','m_dep','mobile_wt','n_cores','pc','px_width','ram','sc_h','sc_w','talk_time','three_g','touch_screen','wifi']

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict',methods=['POST'])
def predict():
    int_features = [x for x in request.form.values()]
    final = np.array(int_features)
    data_unseen = pd.DataFrame([final], columns = cols)
    prediction = predict_model(model, data=data_unseen, round = 0)
    prediction = int(prediction.Label[0])
    return render_template('home.html',pred='Price Range {}'.format(prediction))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    data_unseen = pd.DataFrame([data])
    prediction = predict_model(model, data=data_unseen)
    output = prediction.Label[0]
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
