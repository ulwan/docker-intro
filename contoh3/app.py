import os
import pickle
from flask import Flask, request, jsonify
from google.cloud import storage
from mongo_connector import save_to_mongo


MODEL_NAME = os.environ["MODEL_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
BUCKET_DEST = os.environ["BUCKET_DEST"]
MODEL_NAME = os.environ["MODEL_NAME"]

app = Flask(__name__)

if MODEL_NAME not in os.listdir():
    print("downloading model ...")
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(BUCKET_DEST)
    blob.download_to_filename(f"./{MODEL_NAME}")

models = pickle.load(open("rf_model.pkl", 'rb'))


@app.route('/predict', methods=['POST'])
def is_cancel():
    payload = request.get_json()
    category = {0: "No", 1: "Yes"}
    result_cat = models.predict([list(payload.values())])
    result_prob = models.predict_proba([list(payload.values())])
    res_cat = result_cat.tolist()[0]
    res_prob = result_prob.tolist()[0]
    res = {"is_cancelled": category[res_cat], "is_cancelled_prob": res_prob[res_cat]}
    payload.update(res)
    save_to_mongo(payload)
    return jsonify(res)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=True)
