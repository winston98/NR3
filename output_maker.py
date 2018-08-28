class outputMaker:

    whitelist = ["aluminum", "boron", "calcium", "copper", "iron", "k2o - total",
                 "magnesium", "manganese", "nitrogen - total", "p2o5 - total",
                 "sodium", "sulfur", "zinc"]

    def __init__(self, data, tons):
        self.data = data
        self.output = {}
        self.tons = tons

    def makeSubEntry(self, key, value):
        entry = {}
        entry["analyte"] = key
        entry["asReceived%"] = value
        entry["lbs/ton"] = 2000 * entry["asReceived%"] / 100
        entry["lbs/day"] = self.tons * entry["lbs/ton"]
        # N2O & CO2 equivalent only matters for N and NH3
        if "nitrogen" in key or "ammonia" in key:
            entry["lbs/dayNO2"] = 1.3634 * entry["lbs/day"]
            entry["lbs/dayCO2"] = 298 * entry["lbs/dayNO2"]
            entry["tons/yrCO2"] = 365 * entry["lbs/dayCO2"] / 2000
        self.output[key] = entry
    
    def makeTotalCO2(self):
        lbsPerTon = self.output["total carbon"] / 100 * 2000
        CO2ToCarbon = 11 / 3    # Ratio of molecular weight   
        self.output["totalCO2"] = lbsPerTon * self.tons * CO2ToCarbon

    def makeOutput(self):
        self.output["sampleName"] = self.data["sampleName"]
        for key in self.data:
            value = self.data[key]
            if key in outputMaker.whitelist:
                self.makeSubEntry(key, value)
            else:
                self.output[key] = value
        self.makeTotalCO2()
        
    def getOutput(self):
        return self.output
    
    
