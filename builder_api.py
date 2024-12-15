from flask import Flask, request, jsonify
import builder
import configurator.configurator as conf


app = Flask(__name__)

@app.route("/")
def star():
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



@app.route("/all_mb", methods=['GET']) # TESTING
def all_mb():
    c = conf.Configurator()
    return c.getNamesMB()


@app.route("/configurator", methods=["GET"]) # TESTING...
def configurator():
    data = request.get_json()

    if not data:
        data = {}
    else:
        data = dict(data)

    c = conf.Configurator(data)
    return str(c.filters)


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
