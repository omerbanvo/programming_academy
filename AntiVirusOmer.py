from pathlib import Path
import requests
import time



#פעולה שעוברת על כל הקבצים ב PATH מסויים
def scan_all_folders(path):
    folder = Path(path)
    for item in folder.iterdir():
        if item.is_file():
            print(item)
        else:
            scan_all_folders(Path(item).resolve())

apikey = "fbca160cd1a06bcc1bf2f804193a6ea2c3b3e68590091aa9af2430b9374553d5"
#פעולה ששולחת קובץ לווירוסטוטאל במדפיסה האם הוא תקין או לא..
def send_to_virustotal(apikey, file):
    print(f"waiting for {file} to upload....")
    headers = {"x-apikey": apikey}
    file = Path(file).read_bytes()
    files = {"file":file}
    response = requests.post(url = "https://www.virustotal.com/api/v3/files", headers = headers,files= files)
    print(response.status_code)
    if response.status_code == 200:
        print("upload succesfull")
    else:
        print("there is an error with uploading the file.")
        return
    data = response.json()
    analysis_id = data["data"]["id"]
    print("waiting for scan....")
    response = requests.get(url=f"https://www.virustotal.com/api/v3/analyses/{analysis_id}", headers= headers)
    data = response.json()
    status = data["data"]["attributes"]["status"]

    if(response.status_code != 200):
        print("unable to scan the file.")
        return 
    while status != "completed":
        print(f"still analyzing... status: {status}")
        time.sleep(5)
        response = requests.get(url=f"https://www.virustotal.com/api/v3/analyses/{analysis_id}", headers= headers)
        if(response.status_code != 200):
                print("unable to scan the file.")
                return 
        data = response.json()
        status = data["data"]["attributes"]["status"]


    print("scan completed.")
    stats = data["data"]["attributes"]["stats"]
    
    print("\nScan results:\n")
    print(f"malicious:   {stats['malicious']}  - number of engines that flagged the file as an active threat")
    print(f"suspicious:  {stats['suspicious']} - number of engines that flagged the file as suspicious, without full certainty")
    print(f"harmless:    {stats['harmless']}   - number of engines that actively checked and confirmed the file is safe")
    print(f"undetected:  {stats['undetected']} - number of engines that didn't flag anything unusual (not necessarily safe, just no detection)")
    print(f"timeout:     {stats['timeout']}    - number of engines that didn't finish the check in time")

    total_engines = sum(stats.values())
    print(f"\n{stats['malicious']} out of {total_engines} engines flagged this file as malicious")


        

send_to_virustotal( apikey,
    "/Users/omerbanvolgyi/Documents/personal/index.html")
    



