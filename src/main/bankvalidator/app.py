from flask import Flask, render_template, request
from config import configure_app

app = Flask(__name__)
configure_app(app)

from services import modelService


@app.route('/')
def index():
    return render_template("layout.html", len=len(modelService.unique_field), fields=modelService.all_columns,
                           select=modelService.unique_field)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    list_data = []

    for columns in modelService.all_columns:
        list_data.append(modelService.indexOf(data[columns],modelService.unique_order))

    return str(modelService.predict(list_data))


@app.route('/train', methods=['POST'])
def train():
    modelService.train()
    return str(modelService.unique_field)


@app.route('/testing', methods=['GET'])
def testing():
    return str(modelService.testing())


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
