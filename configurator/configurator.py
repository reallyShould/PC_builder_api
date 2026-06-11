from . import constants as cons
import pandas as pd
from functools import reduce
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
        
        if len(req) > 1:
            self.setup()
        else:
            self.filtred = False
        print(jsonify(self.req))

    def getNamesALL(self, dataset):
        data_map = {
            "cpu": cons.cpu_data,
            "gpu": cons.gpu_data,
            "mb": cons.mb_data,
            "ram": cons.ram_data,
            "psu": cons.psu_data,
            "rom": cons.rom_data
        }
        try:
            out_json = {i: name for i, name in enumerate(data_map[dataset]["name"])}
            return jsonify(out_json)
        except:
            return jsonify({"error": "Неверные данные", "status": 400}), 400
    
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
        if self.filters["ram_type"] == "None":
            self.filters["ram_type"] = mb["ramType"].values[0]
        self.filters["power_pin"] = mb["powerPin"].values[0]

    def setCPU(self):
        cpu = cons.cpu_data.loc[cons.cpu_data["id"] == self.req["CPU"]]
        self.filters["socket"] = cpu["socket"].values[0]
        if self.filters["ram_type"] == "None":
            self.filters["ram_type"] = cpu["ramType"].values[0]
        self.filters["TDP"] += int(cpu["TDP"].values[0])

    def setGPU(self):
        gpu = cons.gpu_data.loc[cons.gpu_data["id"] == self.req["GPU"]]
        self.filters["TDP"] += int(gpu["TDP"].values[0])

    def setRAM(self):
        ram = cons.ram_data.loc[cons.ram_data["id"] == self.req["RAM"]]
        if self.filters["ram_type"] == "None":
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

        # TODO Style fix
    
        response = {}
        for i in range(len(tmp_data)):
            response[int(tmp_data["id"].values[i])] = tmp_data["name"].values[i]
        return response

    def getFiltredCPU(self):
        socket = self.filters.get("socket")
        ram_type = self.filters.get("ram_type")

        mask = pd.Series(True, index=cons.cpu_data.index)

        if socket not in (None, "None"):
            mask &= (cons.cpu_data["socket"] == socket)

        if ram_type not in (None, "None"):
            if ram_type == "DDR4/DDR5":
                mask &= cons.cpu_data["ramType"].isin(["DDR4", "DDR5", "DDR4/DDR5"])
            else:
                mask &= (cons.cpu_data["ramType"] == ram_type) | (cons.cpu_data["ramType"] == "DDR4/DDR5")

        tmp_data = cons.cpu_data.loc[mask]
        return dict(zip(tmp_data["id"].astype(int), tmp_data["name"])) # TODO copy style to other

    def getFiltredRAM(self):
        ram_type = self.filters.get("ram_type")

        mask = pd.Series(True, index=cons.ram_data.index)

        if ram_type not in (None, "None"):
            if ram_type == "DDR4/DDR5":
                mask &= cons.ram_data["type"].isin(["DDR4", "DDR5"])
            else:
                mask &= (cons.ram_data["type"] == ram_type)
        tmp_data = cons.ram_data.loc[mask]
        return dict(zip(tmp_data["id"].astype(int), tmp_data["name"]))
    
    def getFiltredGPU(self):
        tmp_data = cons.gpu_data

        # TODO Test

        response = {}
        for i in range(len(tmp_data)):
            response[int(tmp_data["id"].values[i])] = tmp_data["name"].values[i]
        return response

    def getFiltredPSU(self):
        tmp_data = cons.psu_data.loc[(cons.psu_data["power"] >=  self.filters["TDP"])]

        # TODO Test

        response = {}
        for i in range(len(tmp_data)):
            response[int(tmp_data["id"].values[i])] = tmp_data["name"].values[i]
        return response

    def getIdByName(self, name: str) -> int:
        dfs_to_combine = [
            df[["id", "name"]]
            for df in [
                cons.psu_data,
                cons.ram_data,
                cons.gpu_data,
                cons.cpu_data,
                cons.mb_data,
                cons.rom_data,
            ]
        ]

        data_all = pd.concat(dfs_to_combine, ignore_index=True).drop_duplicates()

        result = data_all[data_all["name"].str.strip().str.lower() == name.strip().lower()]

        if not result.empty:
            return int(result["id"].iloc[0])

        return -1
