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
            "TDP":100
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
            self.setCPU()
        if self.req["GPU"] != "None":
            self.setGPU()
        if self.req["RAM"] != "None":
            self.setRAM()
        if self.req["PSU"] != "None":
            self.setPSU()

    def setMB(self):
        mb = cons.mb_data.loc[cons.mb_data["id"] == self.req["MB"]]
        self.filters["socket"] = mb["socket"].values[0]
        self.filters["ram_type"] = mb["ramType"].values[0]
        self.filters["power_pin"] = mb["powerPin"].values[0]

    def setCPU(self):
        cpu = cons.cpu_data.loc[cons.cpu_data["id"] == self.req["CPU"]]
        self.filters["socket"] = cpu["socket"].values[0]
        self.filters["TDP"] += int(cpu["TDP"].values[0])

    def setGPU(self):
        gpu = cons.gpu_data.loc[cons.gpu_data["id"] == self.req["GPU"]]
        self.filters["TDP"] += int(gpu["TDP"].values[0])

    def setRAM(self):
        ram = cons.ram_data.loc[cons.ram_data["id"] == self.req["RAM"]]
        self.filters["ram_type"] = ram["type"].values[0]

    def setPSU(self):
        psu = cons.psu_data.loc[cons.psu_data["id"] == self.req["PSU"]]
        self.filters["TDP"] -= int(psu["power"].values[0])

    def getFiltredMB(self):
        if self.filters["socket"] != "None" and self.filters["ram_type"] != "None":
            tmp_data = cons.mb_data.loc[
                (cons.mb_data["ramType"] == self.filters["ram_type"]) & 
                (cons.mb_data["socket"] == self.filters["socket"])
            ]
        elif self.filters["socket"] != "None":
            tmp_data = cons.mb_data.loc[cons.mb_data["socket"] == self.filters["socket"]]
        elif self.filters["ram_type"] != "None":
            tmp_data = cons.mb_data.loc[cons.mb_data["ramType"] == self.filters["ram_type"]]
        else:
            tmp_data = cons.mb_data

    
        response = {}
        for i in range(len(tmp_data)):
            response[int(tmp_data["id"].values[i])] = tmp_data["name"].values[i]
        return response

    def getFiltredCPU(self):
        if self.filters["socket"] != "None":
            tmp_data = cons.cpu_data.loc[(cons.cpu_data["socket"] == self.filters["socket"])]
        else:
            tmp_data = cons.cpu_data

        response = {}
        for i in range(len(tmp_data)):
            response[int(tmp_data["id"].values[i])] = tmp_data["cpuName"].values[i]
        return response

    def getFiltredRAM(self):
        if self.filters["ram_type"] != "None":
            tmp_data = cons.ram_data.loc[(cons.ram_data["type"] == self.filters["ram_type"])]
        else:
            tmp_data = cons.ram_data

        response = {}
        for i in range(len(tmp_data)):
            response[int(tmp_data["id"].values[i])] = tmp_data["name"].values[i]
        return response
    
    def getFiltredGPU(self):
        tmp_data = cons.gpu_data

        response = {}
        for i in range(len(tmp_data)):
            response[int(tmp_data["id"].values[i])] = tmp_data["gpuName"].values[i]
        return response

    def getFiltredPSU(self):
        tmp_data = cons.psu_data.loc[(cons.psu_data["power"] >=  self.filters["TDP"])]

        response = {}
        for i in range(len(tmp_data)):
            response[int(tmp_data["id"].values[i])] = tmp_data["name"].values[i]
        return response

    def getIdByName(self): # for front
        pass