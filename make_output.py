import json
import os
from datetime import date
import tkinter as tk
from tkinter.filedialog import askopenfilename
from output_maker import outputMaker

def callback():
    # Let user choose data file
    dataPath = os.path.join(os.getcwd(), "data")
    dataFile = tk.filedialog.askopenfilename(initialdir = dataPath,
                               filetypes = [("JSON Files", "*.json")],
                               title = "Choose a file.")
    tons = float(tonInput.get())
    data = {}
    with open(dataFile, "r") as file:
        data = json.load(file)
    maker = outputMaker(data, tons)
    maker.makeOutput()
    output = maker.getOutput()
    outputPath = os.path.join(os.getcwd(), "json_outputs", 
                              output["sampleName"] + "-output-" +
                              date.today().isoformat() + ".json")
    with open(outputPath, "w") as outfile:
        json.dump(output, outfile)
        

master = tk.Tk()
master.title("CSV Parser")
tk.Label(master, text="Enter tons today: ").pack()
tonInput = tk.Entry(master)
tonInput.pack()
tonInput.focus_set()
tk.Button(master, text="OK", command=callback).pack()
tk.Button(master, text="Quit", command=master.quit).pack()

tk.mainloop()