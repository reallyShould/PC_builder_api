import pandas as pd
import random, os

class Build:
    def __init__(self, motherboard=None, cpu=None, gpu=None, psu=None, ram=None, sum_price=None, rom=None, cfg=None, mode='Best', ID=None, gpuCFG='Any', cpuCfg='Any'):
        self.motherboard_price = None
        self.cpu_price = None
        self.gpu_price = None
        self.rom_price = None
        self.ram_price = None
        self.psu_price = None
        self.cfg = cfg
        self.sum_price=sum_price
        self.mode = mode
        self.ID = ID
        self.gpuCFG = gpuCFG
        self.cpuCFG = cpuCfg

        if cfg == "Gaming":
            self.MB_per = 13
            self.CPU_per = 13
            self.GPU_per = 35
            self.PSU_per = 11
            self.RAM_per = 11
            self.ROM_per = 9
            self.Other_per = 8
        elif cfg == "Working":
            self.MB_per = 13
            self.CPU_per = 26
            self.GPU_per = 22
            self.PSU_per = 9
            self.RAM_per = 13
            self.ROM_per = 10
            self.Other_per = 7
        elif cfg == "Graphics":
            self.MB_per = 11
            self.CPU_per = 13
            self.GPU_per = 37
            self.PSU_per = 10
            self.RAM_per = 12
            self.ROM_per = 10
            self.Other_per = 7
        else:
            self.MB_per = 10
            self.CPU_per = 10
            self.GPU_per = 10
            self.PSU_per = 10
            self.RAM_per = 10
            self.ROM_per = 10
            self.Other_per = 10

        self.motherboard = motherboard
        self.cpu = cpu
        self.gpu = gpu
        self.psu = psu
        self.ram = ram
        self.rom = rom
        self.sum_price = sum_price

        self.set_price()

    def set_price(self):
        self.motherboard_price = (int((self.sum_price / 100) * (self.MB_per - 2)), int((self.sum_price / 100) * self.MB_per))
        self.cpu_price = (int((self.sum_price / 100) * (self.CPU_per - 30)), int((self.sum_price / 100) * self.CPU_per))
        self.gpu_price = (int((self.sum_price / 100) * (self.GPU_per - 30)), int((self.sum_price / 100) * self.GPU_per))
        self.rom_price = (int((self.sum_price / 100) * (self.ROM_per - 30)), int((self.sum_price / 100) * self.ROM_per))
        self.ram_price = (int((self.sum_price / 100) * (self.RAM_per - 30)), int((self.sum_price / 100) * self.RAM_per))
        self.psu_price = (int((self.sum_price / 100) * (self.PSU_per - 30)), int((self.sum_price / 100) * self.PSU_per))
        self.other_price = int((self.sum_price / 100) * self.Other_per)
    
    def getCPUnMB(self):
        dfCPU = pd.read_csv("data/CPU.csv")
        if self.cpuCFG == 'AMD':
            to_price_CPU = dfCPU[(dfCPU['price'] > self.cpu_price[0]) & (dfCPU['price'] < self.cpu_price[1]) & (dfCPU['brnd'] == 'AMD')]
        elif self.cpuCFG == 'INTEL':
            to_price_CPU = dfCPU[(dfCPU['price'] > self.cpu_price[0]) & (dfCPU['price'] < self.cpu_price[1]) & (dfCPU['brnd'] == 'Intel')]
        else:
            to_price_CPU = dfCPU[(dfCPU['price'] > self.cpu_price[0]) & (dfCPU['price'] < self.cpu_price[1])]
        to_price_CPU.sort_values('cpuValue')

        if self.mode == 'Best of seven':
            randomTMP = random.randint(1, 7)
            cpu = to_price_CPU.iloc[[randomTMP]]
            while len(cpu['cpuName'].values[0]) < 4:
                randomTMP -= 1
        else:
            cpu = to_price_CPU.head(1)
        try:
            cpu = cpu.drop(columns='Unnamed: 0')
        except:
            pass
        
        self.cpu = Cpu(name=cpu['cpuName'].values[0], 
                       price=cpu['price'].values[0], 
                       mark=cpu['cpuMark'].values[0], 
                       tdp=cpu['TDP'].values[0], 
                       cores=cpu['cores'].values[0], 
                       socket=cpu['socket'].values[0], 
                       category=cpu['category'].values[0])
        
        dfMB = pd.read_csv("data/MB.csv")
        to_price_MB = dfMB[(dfMB['price'] > self.ram_price[0]) & (dfMB['price'] < self.ram_price[1]) & (self.cpu.socket == dfMB["socket"])]
        
        to_price_MB = to_price_MB.sort_values('price', ascending=False)

        mb = to_price_MB.head(1)
        print(mb.head())
        try:
            cpu = cpu.drop(columns='Unnamed: 0')
        except:
            pass
        
        self.motherboard = Motherboard(name=mb['name'].values[0],
                                       formFactor= mb['formFactor'].values[0],
                                       socket= mb['socket'].values[0],
                                       chipset= mb['chipset'].values[0],
                                       ramType= mb['ramType'].values[0],
                                       ramSlots= mb['ramSlots'].values[0],
                                       ramFreq= mb['ramFreq'].values[0],
                                       maxRam= mb['maxRam'].values[0],
                                       powerPin= mb['powerPin'].values[0],
                                       price= mb['price'].values[0])

    def getGPU(self):
        dfGPU = pd.read_csv("data/GPU.csv")
        if self.gpuCFG == 'NVIDIA':
            to_price_GPU = dfGPU[(dfGPU['price'] > self.gpu_price[0]) & (dfGPU['price'] < self.gpu_price[1]) & (dfGPU['brnd'] == 'NVIDIA')]
        elif self.gpuCFG == 'AMD':
            print('AMD')
            to_price_GPU = dfGPU[(dfGPU['price'] > self.gpu_price[0]) & (dfGPU['price'] < self.gpu_price[1]) & (dfGPU['brnd'] == 'AMD')]
        else:
            to_price_GPU = dfGPU[(dfGPU['price'] > self.gpu_price[0]) & (dfGPU['price'] < self.gpu_price[1])]
        to_price_GPU.sort_values('gpuValue')

        if self.mode == 'Best of seven':
            randomTMP = random.randint(1, 7)
            gpu = to_price_GPU.iloc[[randomTMP]]
            while len(gpu['gpuName'].values[0]) < 4:
                randomTMP -= 1
        else:
            gpu = to_price_GPU.head(1)

        try:
            gpu = gpu.drop(columns='Unnamed: 0')
        except:
            pass
        self.gpu = Gpu(name=gpu['gpuName'].values[0], 
                       price=gpu['price'].values[0], 
                       mark3D=gpu['G3Dmark'].values[0], 
                       mark2D=gpu['G2Dmark'].values[0], 
                       tdp=gpu['TDP'].values[0],                        
                       category=gpu['category'].values[0])

    def getROM(self, dbl=False, remainder=0):
        dfROM = pd.read_csv("data/ROM.csv")
        if self.cfg == "Gaming" and dbl:
            to_price_ROM = dfROM[(dfROM['price'] <= remainder) & (dfROM['type'] == 'SSD') & (dfROM['diskCapacity'] > 1000)]
            if len(to_price_ROM['type'].values) == 0:
                to_price_ROM = dfROM[(dfROM['price'] <= remainder) & (dfROM['diskCapacity'] > 2000)]
        elif self.cfg == "Gaming" and not dbl:
            to_price_ROM = dfROM[(dfROM['price'] > self.rom_price[0]) & (dfROM['price'] < self.rom_price[1]) & (dfROM['type'] == 'SSD')]
            if len(to_price_ROM['type'].values) == 0:
                to_price_ROM = dfROM[(dfROM['price'] > self.rom_price[0]) & (dfROM['price'] < self.rom_price[1])]
        else:
            to_price_ROM = dfROM[(dfROM['price'] > self.rom_price[0]) & (dfROM['price'] < self.rom_price[1])]
        to_price_ROM.sort_values('driveValue')

        rom = to_price_ROM.head(1)
        try:
            cpu = cpu.drop(columns='Unnamed: 0')
        except:
            pass
        if not dbl:
            self.rom = Rom(name=rom['driveName'].values[0],
                        type=rom['type'].values[0],
                        capacity=rom['diskCapacity'].values[0],
                        mark=rom['diskMark'].values[0],
                        rank=rom['rank'].values[0],
                        price=rom['price'].values[0])
        elif dbl:
            self.rom = Rom(name=rom['driveName'].values[0],
                        type=rom['type'].values[0],
                        capacity=rom['diskCapacity'].values[0],
                        mark=rom['diskMark'].values[0],
                        rank=rom['rank'].values[0],
                        price=rom['price'].values[0])
        else:
            print('Что то пошло не так')

    def getTDP(self):
        open(f'{os.getcwd()}\\userdata\\{self.ID}\\TDP.txt', 'a+').write(str(self.cpu.tdp + self.gpu.tdp + 400))

    def getPSU(self):
        dfPSU = pd.read_csv("data/PSU.csv")

        to_price_PSU = dfPSU[(dfPSU['price'] > self.psu_price[0]) & (dfPSU['price'] < self.psu_price[1]) & (dfPSU['power'] > int(open(f'{os.getcwd()}\\userdata\\{self.ID}\\TDP.txt').read()[0:-2]))]
        try:
            os.remove(f'{os.getcwd()}\\userdata\\{self.ID}\\TDP.txt')
        except:
            print('rm err')

        to_price_PSU.sort_values('value')

        psu = to_price_PSU.head(1)

        self.psu = Psu(name=psu['name'].values[0],
                       formFactor=psu['formFactor'].values[0],
                       power=psu['power'].values[0],
                       fan=psu['fan'].values[0],
                       pin=psu['pin'].values[0],
                       gpuPin=psu['GPUpin'].values[0],
                       price=psu['price'].values[0]
                       )

    def getRAM(self, dbl=False, remainder=0):
        dfRAM = pd.read_csv('data/RAM.csv')

        if dbl:
            to_price_RAM = dfRAM[(dfRAM['price'] > self.ram_price[0]) & (dfRAM['price'] < self.ram_price[1]) & (dfRAM['type'] == self.motherboard.ramType) 
                                 & (dfRAM['count'] == 2 if self.motherboard.ramSlots == 2 else dfRAM['count'] == 4) & (dfRAM['capacity'] >= 16 if self.motherboard.ramSlots == 2 else dfRAM['capacity'] == 8)]
            to_price_RAM.sort_values('value')
            ram = to_price_RAM.head(1)
            
            if len(ram) == 0 and self.motherboard.ramSlots == 4:
                to_price_RAM = dfRAM[(dfRAM['price'] > self.ram_price[0]) & (dfRAM['price'] < self.ram_price[1]) & (dfRAM['type'] == self.motherboard.ramType)]
                to_price_RAM.sort_values('value')
                ram = to_price_RAM.head(1)
                
                if ram['price'].values[0]*2 < self.ram_price[1] + remainder/2:
                    print(ram['price'].values[0]*2)
                    print(self.ram_price[1] + remainder/2)
                    self.ram = Ram(name=ram['name'].values[0],
                        count=ram['count'].values[0]*2,
                        capacity=ram['capacity'].values[0],
                        freq=ram['freq'].values[0],
                        timings=ram['timings'].values[0],
                        formFactor=ram['formFactor'].values[0],
                        type=ram['type'].values[0],
                        price=ram['price'].values[0]*2
                        )
                    return 0;
                else:
                    to_price_RAM = dfRAM[(dfRAM['price'] > self.ram_price[0]) & (dfRAM['price'] < self.ram_price[1]) & (dfRAM['type'] == self.motherboard.ramType)]
            elif len(ram) == 0 and self.motherboard.ramSlots == 2:
                to_price_RAM = dfRAM[(dfRAM['price'] > self.ram_price[0]) & (dfRAM['price'] < self.ram_price[1]) & (dfRAM['type'] == self.motherboard.ramType)]
        else:
            to_price_RAM = dfRAM[(dfRAM['price'] > self.ram_price[0]) & (dfRAM['price'] < self.ram_price[1]) & (dfRAM['type'] == self.motherboard.ramType)]

        to_price_RAM.sort_values('value')
        print(to_price_RAM.head())
        ram = to_price_RAM.head(1)
        print(ram)
        
        self.ram = Ram(name=ram['name'].values[0],
                       count=ram['count'].values[0],
                       capacity=ram['capacity'].values[0],
                       freq=ram['freq'].values[0],
                       timings=ram['timings'].values[0],
                       formFactor=ram['formFactor'].values[0],
                       type=ram['type'].values[0],
                       price=ram['price'].values[0]
                       )

    def get_json(self):
        pc_price = round(float(self.cpu.price + self.gpu.price + self.motherboard.price + self.rom.price + self.psu.price + self.ram.price), 2)
        return {
            "cpu": {
                "name": self.cpu.name,
                "socket": self.cpu.socket,
                "cores": int(self.cpu.cores),
                "tdp": int(self.cpu.tdp),
                "bench": int(self.cpu.mark),
                "price": float(self.cpu.price)
            },
            "gpu": {
                "name": self.gpu.name,
                "tdp": int(self.gpu.tdp),
                "bench3d": int(self.gpu.mark3D),
                "bench2d": int(self.gpu.mark2D),
                "price": float(self.gpu.price)
            },
            "motherboard": {
                "name": self.motherboard.name,
                "form": self.motherboard.formFactor,
                "socket": self.motherboard.socket,
                "chipset": self.motherboard.chipset,
                "ramType": self.motherboard.ramType,
                "ramSlots": int(self.motherboard.ramSlots),
                "ramFreq": int(self.motherboard.ramFreq),
                "maxRam": int(self.motherboard.maxRam),
                "powerPin": self.motherboard.powerPin,
                "price": float(self.motherboard.price)
            },
            "ram": {
                "name": self.ram.name,
                "type": self.ram.type,
                "count": int(self.ram.count),
                "capacity": int(self.ram.capacity),  
                "freq": int(self.ram.freq),          
                "time": self.ram.timings,
                "form": self.ram.formFactor,
                "price": float(self.ram.price)       
            },
            "rom": {
                "name": self.rom.name,
                "type": self.rom.type,
                "capacity": int(self.rom.capacity),  
                "bench": int(self.rom.mark),         
                "price": float(self.rom.price)       
            },
            "psu": {
                "name": self.psu.name,
                "form": self.psu.formFactor,
                "power": int(self.psu.power),        
                "fan": self.psu.fan,
                "pin": self.psu.pin,
                "gpuPin": self.psu.gpuPin,
                "price": float(self.psu.price)       
            },
            "settings": {
                "config": self.cfg,
                "mode": self.mode
            },
            "other": round(float(self.sum_price - pc_price), 1),        
            "price": pc_price
        }


    def build(self): 
        self.getCPUnMB()
        self.getGPU()
        self.getROM()
        self.getTDP()
        self.getPSU()
        self.getRAM()
        tmpPrice = self.cpu.price + self.gpu.price + self.motherboard.price + self.rom.price + self.psu.price + int(self.ram.price) + self.other_price
        if tmpPrice < self.sum_price:
            remainder = self.sum_price - tmpPrice
            if remainder > 4000:
                self.getROM(dbl=True, remainder=remainder/2)
                self.getRAM(dbl=True, remainder=remainder/2)
    

class Motherboard:
    def __init__(self, name=None, formFactor=None, socket=None, chipset=None, ramType=None, ramSlots=0, ramFreq=0, maxRam=0, powerPin=None, price=0, category=None):
        self.name = name
        self.formFactor = formFactor
        self.socket = socket
        self.chipset = chipset
        self.ramType = ramType
        self.ramSlots = ramSlots
        self.ramFreq = ramFreq
        self.price = price
        self.category = category
        self.maxRam = maxRam
        self.powerPin = powerPin


class Cpu:
    def __init__(self, name=None, price=0, mark=0, tdp=0, cores=0, socket=None, category=None):
        self.name = name
        self.price = price
        self.mark = mark
        self.tdp = tdp
        self.cores = cores
        self.socket = socket
        self.category = category


class Gpu:
    def __init__(self, name=None, price=0, mark3D=0, mark2D=0, tdp=0, category=None):
        self.name = name
        self.price = price
        self.mark3D = mark3D
        self.mark2D = mark2D
        self.tdp = tdp
        self.category = category


class Rom:
    def __init__(self, name=None, type=None, capacity=0, price=0, mark=0, rank=0, count=1):
        self.name = name
        self.type = type
        self.capacity = capacity
        self.price = price
        self.mark = mark
        self.rank = rank
        self.count = count
    

class Psu:
    def __init__(self, name=None, formFactor=None, power=None, fan=None, pin=None, gpuPin=None, price=None):
        self.name = name
        self.formFactor = formFactor
        self.power = power
        self.fan = fan
        self.pin = pin
        self.gpuPin = gpuPin
        self.price = price

class Ram:
    def __init__(self, name=None, count=None, capacity=None, freq=None, timings=None, formFactor=None, type=None, price=None):
        self.name = name
        self.count = count
        self.capacity = capacity
        self.freq = freq
        self.timings = timings
        self.formFactor = formFactor
        self.type = type
        self.price = price
        
