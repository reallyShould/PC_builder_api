import constants as cons
import pandas as pd
from flask import jsonify

# print(cons.mb_data["link"][0])

class Configurator:
    def __init__(self):
        pass

    def getNamesMB(self):
        out_json = {}
        mb_data_len = len(cons.mb_data)
        for i in range(mb_data_len):
            out_json[i] = cons.mb_data["name"][i]
        return jsonify(out_json)