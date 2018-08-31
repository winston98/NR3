import csv
import json
import os
import glob
import fetchemail

def update():
    file_list = glob.glob(os.path.join(download_path, "*"))
    newestFile = max(file_list, key=os.path.getctime)
    with open(newestFile, "r") as newCSV:
        reader = csv.reader(newCSV)
        for row in reader:
            sampleName = row[1]
            # skip header row
            if sampleName == "Sample Name":
                continue
            test = row[8].lower()
            value = row[9]
            date = row[3]           
            # drop "<" sign
            if "<" in value:
                value = value[1:]
            # if value is numeric, cast to double
            try:
                value = float(value)
            except ValueError:
                pass
            dataPath = os.path.join(os.getcwd(), "data", sampleName + ".json")
            dataObject = {}
            # if no data file exists for this sample name, then create that file
            try:
                with open(dataPath, "r") as file:
                    dataObject = json.load(file)
            except:
                pass
            with open(dataPath, "w") as file:
                dataObject["sampleName"] = sampleName
                dataObject["testDate"] = date
                dataObject[test] = value
                json.dump(dataObject, file)

# On startup, download attatchments from unread files
download_path = os.path.join(os.getcwd(),"downloads")
mail_server = "imap.gmail.com"
username = "testdata@nr3llc.com"
password = "ceshishuju"
emailFetcher = fetchemail.FetchEmail(mail_server, username, password)
for email in emailFetcher.fetch_unread_messages():
    emailFetcher.save_attachment(email,download_path)
    update()
emailFetcher.close_connection()

update()