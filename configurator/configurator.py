from . import constants as cons
import pandas as pd
from flask import jsonify

class Configurator:
    def __init__(self, mbid=-1, cpuid=-1, gpuid=-1, ramid=-1, romid=-1, psuid=-1): # NO NO NO! use list?
        self.mbid = mbid
        self.cpuid = cpuid
        self.gpuid = gpuid
        self.ramid = ramid
        self.romid = romid
        self.psuid = psuid

        unnamed = { # req
            "socket":"None",
            "ram_type":"None"
        }

    def getNamesMB(self):
        out_json = {}
        mb_data_len = len(cons.mb_data)
        for i in range(mb_data_len):
            out_json[i] = cons.mb_data["name"][i]
        return jsonify(out_json)
    