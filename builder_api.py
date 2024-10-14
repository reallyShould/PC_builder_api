from flask import Flask, request, jsonify
import builder
import configurator.configurator as conf


app = Flask(__name__)


@app.route("/build", methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
