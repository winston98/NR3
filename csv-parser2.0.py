import csv
from tkinter import *


master = Tk()
master.title("CSV Parser")
Label(master, text="Enter file name: ").pack()
f_input = Entry(master)
f_input.pack()
f_input.focus_set()
Label(master, text="Enter tons today: ").pack()
t_input = Entry(master)
t_input.pack()
t_input.focus_set()

moisture = 0.0
output = []

"""def contains(string, regex):
    if(re.search(regex, string, re.IGNORECASE) == None):
        return False
    else:
        return True"""

def makeRow(analyte, data):
    analyte_lower = analyte.lower()
    row = []
    if "nitrogen" not in analyte_lower and "ammonia" not in analyte_lower:
        data /= 10000
    row.append(analyte) # analyte type
    row.append(data) # dry basis%
    row.append(moisture) # moisture    
    row.append(data * (1 - moisture/100)) # as recieved
    lbs = 2000 * row[3] / 100
    if "potassium" in analyte_lower: # 1:1.2046 K to K2O
        lbs *= 1.2046
    elif "phosphorus" in analyte_lower: # 1:2.2914 P to P2O5
        lbs *= 2.2914
    row.append(lbs) # lbs/ton
    row.append(float(t_input.get())) # tons/day, user input
    row.append(24 * row[4]) # lbs/day
    row.append(365 * row[6]) # lbs/yr
    # N2O & CO2 equivalent only matters for N and NH3
    if "nitrogen" in analyte_lower or "ammonia" in analyte_lower:
        row.append(1.3634 * row[6]) # N2O lbs/day
        row.append(298 * row[8]) # CO2 lbs/day
        row.append(365 * row[9] / 2000) #CO2 tons/yr
    return row

# Many unnecessary middle steps in case intermdiate values need displayed
def totalCarbon():
    percentSolid = 100 - moisture
    solidsPerTon = percentSolid / 100 * 2000
    otherSolids = 0
    for row in output:
        otherSolids += row[4]
    carbonPerTon = solidsPerTon - otherSolids
    carbonPerDay = float(t_input.get()) * carbonPerTon / 2000
    co2PerDay = 3.664191096 * carbonPerDay
    return co2PerDay

def callback():
    filename = f_input.get()
    try:
        file = open(filename + ".csv")
    except (OSError, IOError):
        error = Toplevel(master)
        error.title("Error")
        Label(error, text="Invalid filename").pack()    
    
    with file:
        reader = csv.reader(file)
        global moisture
        for row in reader:
            if(row[1] == "Sample Id"): # skip header row
                continue
            analyte = row[12]
            data = float(row[13])
            if "moisture" in analyte.lower():
                moisture = float(row[13])
                continue
            output.append(makeRow(analyte, data))
    # write results to output            
    with open(filename + "-output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["", "Dry Basis %", "Moisture %",
                         "As Received", "lbs/ton", "Tons/day",
                         "lbs/day", "lbs/yr", "N2O lbs/day", 
                         "CO2 lbs/day", "CO2 tons/yr"])
        writer.writerows(output)
        writer.writerow(["CO2 tons/day", totalCarbon()])
        output.clear()


Button(master, text="OK", command=callback).pack()
Button(master, text="Quit", command=master.quit).pack()

mainloop()

