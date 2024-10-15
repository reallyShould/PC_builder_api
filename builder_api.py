from flask import Flask, request, jsonify
import builder
import configurator.configurator as conf


app = Flask(__name__)


## FOR TESTING
# curl -X GET http://127.0.0.1:5000/build -H "Content-Type: application/json" -d '{"price": "50000","cfg":"Gaming"}'


@app.route("/build", methods=['GET'])
def build():
    data = request.get_json()

    if data and "price" in data and "cfg" in data:
        price = int(data["price"])
        cfg = data["cfg"]
        bld = builder.Build(sum_price=price, cfg=cfg)
        bld.build()
        
        return jsonify(bld.get_json())
    else:
        return jsonify({'error': 'No message provided'}), 400

@app.route("/all_mb", methods=['GET']) # TESTING
def all_mb():
    c = conf.Configurator()
    return c.getNamesMB()

## FOR TEST
# curl -X GET http://127.0.0.1:5000/configurator -H "Content-Type: application/json" -d '{"MB": 5}'

@app.route("/configurator", methods=["GET"]) # TESTING...
def configurator():
    data = request.get_json()

    if not data:
        data = {}
    else:
        data = dict(data)

    c = conf.Configurator(data)
    return c.setMB()

if __name__ == '__main__':
    app.run(debug=True)
