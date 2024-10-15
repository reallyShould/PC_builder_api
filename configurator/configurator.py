from . import constants as cons
import pandas as pd
from flask import jsonify

class Configurator:
    def __init__(self, req={}):
        self.req = req
        self.filtred = True
        self.unnamed = {
            "socket":"None",
            "ram_type":"None",
            "power_pin":"None"
        }
        
        if req != {}:
            self.setup()
        else:
            self.filtred = False
        print(jsonify(self.req))

    def getNamesMB(self):
        out_json = {}
        mb_data_len = len(cons.mb_data)
        for i in range(mb_data_len):
            out_json[i] = cons.mb_data["name"][i]
        return jsonify(out_json)
    
    def setup(self):
        if self.req["MB"] != "None":
            self.setMB()

    def setMB(self):
        mb = cons.mb_data.loc[cons.mb_data["id"] == self.req["MB"]]
        self.unnamed["socket"] = mb["socket"].values[0]
        self.unnamed["ram_type"] = mb["ramType"].values[0]
        self.unnamed["power_pin"] = mb["powerPin"].values[0]
        return str(self.unnamed)

    def findCPU(self):
        pass

    def findGPU(self):
        pass

    def findRAM(self):
        pass

    def findPSU(self):
        pass