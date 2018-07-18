import csv
import json
import os
from datetime import date
from tkinter import *
from tkinter.filedialog import askopenfilename
from sample import Sample
from fetchemail import FetchEmail

# On startup, download attatchments from unread files
download_path = os.path.join(os.getcwd(),"downloads")
mail_server = "imap.gmail.com"
username = "testdata@nr3llc.com"
password = "ceshishuju"
emailFetcher = FetchEmail(mail_server, username, password)
for email in emailFetcher.fetch_unread_messages():
    emailFetcher.save_attachment(email,download_path)
emailFetcher.close_connection()

def makeJSON(output):
    path = os.path.join(os.getcwd(), "json_outputs", output["sampleName"] +
                        "-outputs-" + date.today().isoformat() + ".json")
    with open(path, "w") as outfile:
        json.dump(output, outfile)

def makeCSV(output):
    path = os.path.join(os.getcwd(), "csv_outputs", output["sampleName"] +
                        "-outputs-" + date.today().isoformat() + ".csv")
    with open(path, "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Sample Name", output["sampleName"]])
        writer.writerow(["Moisture", output["moisture"]])
        writer.writerow(["Tons/Day", output["tons/day"]])
        writer.writerow(["co2PerDay", output["co2PerDay"]])
        for key in output:
            if key not in ["sampleName", "moisture", "tons/day", "co2PerDay"]:
                row = [key]
                for field in output[key]:
                    row.append(field + ": " + str(output[key][field]))
                writer.writerow(row)

def callback():
    # Let user choose file
    filename = askopenfilename(initialdir=download_path,
                               filetypes =[("CSV Files", "*.csv")],
                               title = "Choose a file.")
    with open(filename) as file:
        reader = csv.reader(file)
        sample = Sample()
        for row in reader:
            if row[1] == "Sample Id": # skip header row
                continue
            elif sample.getName() != row[1]: # sampleName doesn't match
                if sample.getName() != None: # not None means not first sample
                    sample.totalCarbon()
                    makeJSON(sample.getOutput())
                    makeCSV(sample.getOutput())
                    sample = Sample()
                sample.add("sampleName", row[1])
                sample.add("tons/day", float(t_input.get())) # user input
            analyte = row[12]
            data = row[13]
            if "<" in data: # drop "<" sign by flooring
                data = int(float(data[1:]))
            data = float(data)
            if "moisture" in analyte.lower():
                sample.add("moisture", float(row[13]))
                continue
            sample.makeEntry(analyte, data)
        sample.totalCarbon()
        makeJSON(sample.getOutput())
        makeCSV(sample.getOutput())

master = Tk()
master.title("CSV Parser")
Label(master, text="Enter tons today: ").pack()
t_input = Entry(master)
t_input.pack()
t_input.focus_set()
Button(master, text="OK", command=callback).pack()
Button(master, text="Quit", command=master.quit).pack()

mainloop()

