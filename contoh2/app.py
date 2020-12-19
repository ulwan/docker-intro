from flask import Flask, request, jsonify
import logging

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(filename='demo.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


app = Flask(__name__)

@app.route('/', defaults={"name": "World"})
@app.route('/<name>', methods=['GET'])
def data(name):
    data = {
        "Hello": name
    }
    logging.info(data)
    return jsonify(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000)
