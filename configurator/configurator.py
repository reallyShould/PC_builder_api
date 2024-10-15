from . import constants as cons
import pandas as pd
from flask import jsonify

class Configurator:
    def __init__(self, req={}):
        self.req = req
        self.filtred = True
        self.filters = {
            "socket":"None",
            "ram_type":"None",
            "power_pin":"None",
            "TDP":0
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
        if self.req["CPU"] != "None":
            self.setMB()
        if self.req["GPU"] != "None":
            self.setGPU()

    def setMB(self):
        mb = cons.mb_data.loc[cons.mb_data["id"] == self.req["MB"]]
        self.filters["socket"] = mb["socket"].values[0]
        self.filters["ram_type"] = mb["ramType"].values[0]
        self.filters["power_pin"] = mb["powerPin"].values[0]
        return str(self.filters)

    def setCPU(self):
        cpu = cons.cpu_data.loc[cons.cpu_data["id"] == self.req["CPU"]]
        self.filters["socket"] = cpu["socket"].values[0]
        self.filters["TDP"] += int(cpu["TDP"].values[0])
        return str(self.filters)

    def setGPU(self):
        gpu = cons.gpu_data.loc[cons.gpu_data["id"] == self.req["GPU"]]
        self.filters["TDP"] += int(gpu["TDP"].values[0])

    def findRAM(self):
        pass

    def findPSU(self):
        pass

    def getIdByName(self): # for front
        pass