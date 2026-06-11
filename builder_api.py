from flask import Flask, request, jsonify
import builder
import configurator.configurator as conf
from config import HOST, PORT

app = Flask(__name__)

@app.route("/")
def start():
    return "Hello"

@app.route("/build", methods=['POST'])
def build():
    data = request.get_json()

    if data and "price" in data and "cfg" in data:
        price = data["price"]
        cfg = data["cfg"]
        try:
            gpuCFG = data["gpu"]
            cpuCFG = data["cpu"]
            mode = data["mode"]
        except:
            gpuCFG = "Any"
            cpuCFG = "Any"
            mode = "Best"

        if not price or not price.isdigit():
            return jsonify({'error': 'Invalid price value'}), 400

        price = int(price)
        bld = builder.Build(sum_price=price, cfg=cfg, gpuCFG=gpuCFG, cpuCfg=cpuCFG, mode=mode)
        bld.build()

        return jsonify(bld.get_json())
    else:
        return jsonify({'error': 'No message provided'}), 400


@app.route("/all_mb", methods=['GET'])
def all_mb():
    c = conf.Configurator()
    return c.getNamesALL("mb")

@app.route("/all_cpu", methods=['GET'])
def all_cpu():
    c = conf.Configurator()
    return c.getNamesALL("cpu")

@app.route("/all_gpu", methods=['GET'])
def all_gpu():
    c = conf.Configurator()
    return c.getNamesALL("gpu")

@app.route("/all_psu", methods=['GET'])
def all_psu():
    c = conf.Configurator()
    return c.getNamesALL("psu")

@app.route("/all_ram", methods=['GET'])
def all_ram():
    c = conf.Configurator()
    return c.getNamesALL("ram")

@app.route("/all_rom", methods=['GET'])
def all_rom():
    c = conf.Configurator()
    return c.getNamesALL("rom")


@app.route("/configurator", methods=["GET"]) # TODO Remember why this is needed
def configurator():
    data = request.get_json()

    if not data:
        data = {}
    else:
        data = dict(data)

    c = conf.Configurator(data)
    return str(c.filters)


# TODO TRY EXCEPT HERE
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

    # TODO RAM by CPU not work, fix

    c = conf.Configurator(data)
    return jsonify(c.getFiltredRAM())


@app.route("/filter_gpu", methods=["GET"]) #TODO Test it
def filterGPU():
    data = request.get_json()
    data = {} if not data else dict(data)

    c = conf.Configurator(data)
    return jsonify(c.getFiltredGPU())


@app.route("/filter_psu", methods=["GET"]) #TODO Test it
def filterPSU():
    data = request.get_json()
    data = {} if not data else dict(data)

    c = conf.Configurator(data)
    return jsonify(c.getFiltredPSU())

@app.route("/get_id_by_name", methods=["GET"])
def getIdByName():
    data = request.get_json()
    data = {} if not data else dict(data)

    c = conf.Configurator(data)
    return jsonify(c.getIdByName(name=data["name"]))


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
