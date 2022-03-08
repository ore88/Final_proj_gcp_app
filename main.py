import pandas as pd
import numpy as np
from flask import Flask,request, url_for, redirect, render_template, jsonify
import pickle
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/content/drive/MyDrive/gcp_key.json'
storage_client = storage.Client()

CLOUD_PROJECT = 'grand-drive-342813' # GCP project name
bucket_name = 'msdsproject_finlproj' # bucket name for storage of your model
BUCKET = 'gs://' + CLOUD_PROJECT + '-{}'.format(bucket_name)

def download_blob(project_name, bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client(project_name)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    if destination_file_name is not None: 
      blob.download_to_filename(destination_file_name)
      print(
          "Blob {} downloaded to {}.".format(
              source_blob_name, destination_file_name
          )
      )     
    return blob

app = Flask(__name__)

outfile_name = model_dir + 'knn-reg101-gcp-downloaded'
model_gcp_src = str(model_name)+'.pkl'
model_downloaded = download_blob(CLOUD_PROJECT, bucket_name, model_gcp_src, 'knn_model.pkl')

# Loading the model for predictions
model= load_model(knn_model)

# Predictions from deployed model
# new_prediction_gcp = predict_model(gcp_final_knn, data=df_test)

cols = ['battery_power','blue','clock_speed','dual_sim',	
        'fc','four_g','int_memory','m_dep','mobile_wt','n_cores','pc',
        'px_width','ram','sc_h','sc_w','talk_time','three_g','touch_screen',
        'wifi']

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
