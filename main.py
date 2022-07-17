from flask import render_template, request, jsonify
from app_py import app
import process


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


# Object Detection Model
@app.route('/add_product', methods=['POST'])
# @cross_origin(origin='*')
def add_data():
    humidity = float(request.form.get('humidity'))
    temperature = float(request.form.get('temperature'))

    if process.add_data(humidity=humidity, temperature=temperature):
        return jsonify({"status": 200, "message": "Add Successful"})
    return jsonify({"status": 400, "message": "Product already exists!"})


@app.route('/update_product', methods=['POST'])
# @cross_origin(origin='*')
def update_product():
    id_product = request.form.get('id_product')
    name = request.form.get('name')
    price = float(request.form.get('price'))
    unit = request.form.get('unit')
    description = request.form.get('description')

    if process.update_product(id_product=id_product, name=name, price=price, unit=unit, description=description):
        return jsonify({"status": 200, "message": "Change successful!"})
    return jsonify({"status": 400, "message": "Change failed!"})


@app.route('/del_product', methods=['POST'])
# @cross_origin(origin='*')
def del_obmodel():
    id_product = request.form.get('id_product')
    if process.delete_product(id_product=id_product):
        return jsonify({"status": 200, "message": "Delete successful"})
    return jsonify({"status": 400, "message": "Object detection model does not exist!"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
