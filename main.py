import csv
from tkinter import *
from sample import Sample

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
        sample = Sample()
        for row in reader:
            if row[1] == "Sample Id": # skip header row
                continue
            elif sample.getName() != row[1]:
                if sample.getName() != None:
                    sample.totalCarbon()
                    sample.makeFile()
                    sample = Sample()
                sample.add("sampleName", row[1])
                sample.add("tons/day", float(t_input.get())) # user input
            analyte = row[12]
            data = row[13]
            if "<" in data:
                data = int(float(data[1:]))
            data = float(data)
            if "moisture" in analyte.lower():
                sample.add("moisture", float(row[13]))
                continue
            sample.makeEntry(analyte, data)
        sample.totalCarbon()
        sample.makeFile()

Button(master, text="OK", command=callback).pack()
Button(master, text="Quit", command=master.quit).pack()

mainloop()

