import csv
import os
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
                    sample.makeJSON()
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
        sample.makeJSON()

master = Tk()
master.title("CSV Parser")
Label(master, text="Enter tons today: ").pack()
t_input = Entry(master)
t_input.pack()
t_input.focus_set()
Button(master, text="OK", command=callback).pack()
Button(master, text="Quit", command=master.quit).pack()

mainloop()

