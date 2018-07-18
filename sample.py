class Sample:

    def __init__(self):
        self.output = {}
        self.otherSolids = 0.0

    def add(self, key, value):
        self.output[key] = value

    def getName(self):
        if "sampleName" in self.output:
            return self.output["sampleName"]
        else:
            return None

    def makeEntry(self, analyte, data):
        entry = {}
        analyte = analyte.lower()
        if "nitrogen" not in analyte and "ammonia" not in analyte:
            data /= 10000
        entry["dryBasis%"] = data
        entry["asReceived%"] = data * (1 - self.output["moisture"]/100)
        lbs = 2000 * entry["asReceived%"] / 100
        if "potassium" in analyte: # 1:1.2046 K to K2O
            lbs *= 1.2046
        elif "phosphorus" in analyte: # 1:2.2914 P to P2O5
            lbs *= 2.2914
        self.otherSolids += lbs
        entry["lbs/ton"] = lbs
        entry["lbs/day"] = self.output["tons/day"] * lbs
        entry["lbs/yr"] = 365 * entry["lbs/day"]
        # N2O & CO2 equivalent only matters for N and NH3
        if "nitrogen" in analyte or "ammonia" in analyte:
            entry["lbs/dayNO2"] = 1.3634 * entry["lbs/day"]
            entry["lbs/dayCO2"] = 298 * entry["lbs/dayNO2"]
            entry["tons/yrCO2"] = 365 * entry["lbs/dayCO2"] / 2000
        self.output[analyte] = entry

    # Many unnecessary middle steps in case intermdiate values need displayed
    def totalCarbon(self):
        percentSolid = 100 - self.output["moisture"]
        solidsPerTon = percentSolid / 100 * 2000
        carbonPerTon = solidsPerTon - self.otherSolids
        carbonPerDay = self.output["tons/day"] * carbonPerTon / 2000
        co2PerDay = 3.664191096 * carbonPerDay
        self.output["co2PerDay"] = co2PerDay

    def getOutput(self):
        return self.output
