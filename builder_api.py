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
# curl -X GET http://127.0.0.1:5000/configurator -H "Content-Type: application/json" -d '{"MB": 5, "CPU": 63, "GPU": 1, "RAM": 0, "PSU": 0}'

@app.route("/configurator", methods=["GET"]) # TESTING...
def configurator():
    data = request.get_json()

    if not data:
        data = {}
    else:
        data = dict(data)

    c = conf.Configurator(data)
    return str(c.filters)


## FOR TEST
# curl -X GET http://127.0.0.1:5000/filter_mb -H "Content-Type: application/json" -d '{"MB": "None", "CPU": 63, "GPU": "None", "RAM": "None", "PSU": "None"}'

## TRY EXCEPT HERE

@app.route("/filter_mb", methods=["GET"])
def filterMB():
    data = request.get_json()
    data = {} if not data else dict(data)

    c = conf.Configurator(data)
    return jsonify(c.getFiltredMB())


@app.route("/filter_cpu", methods=["GET"])
def filterCPU():
    data = request.get_json()
    data = {} if not data else dict(data)

    c = conf.Configurator(data)
    return jsonify(c.getFiltredCPU())


@app.route("/filter_ram", methods=["GET"])
def filterRAM():
    data = request.get_json()
    data = {} if not data else dict(data)

    c = conf.Configurator(data)
    return jsonify(c.getFiltredRAM())

@app.route("/filter_gpu", methods=["GET"])
def filterGPU():
    data = request.get_json()
    data = {} if not data else dict(data)

    c = conf.Configurator(data)
    return jsonify(c.getFiltredGPU())


@app.route("/filter_psu", methods=["GET"])
def filterPSU():
    data = request.get_json()
    data = {} if not data else dict(data)

    c = conf.Configurator(data)
    return jsonify(c.getFiltredPSU())


if __name__ == '__main__':
    app.run(debug=True)
