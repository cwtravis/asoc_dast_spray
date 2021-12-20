import sys
import os
from ASoC import ASoC


INPUT_FILE_PATH = "example_input.txt"
OUTPUT_FILE_PATH = "InitDAST_Status.csv"
ASOC_APP_ID = "<APP_ID>"
PRESENCE_ID = "<PRESENCE_ID>"

API_KEY = {
  "KeyId": "<KEY_ID>",
  "KeySecret": "<KEY_SECRET>"
}


def readPrevStatus(prevOutputFile):
    pass

def checkScannedAlready(outputFile, url):
    contents = ""
    with open(outputFile, "r") as out:
        contents = out.read()
    return url in contents
    
def writeStatus(outputFile, url, scanId, update):
    file = open(outputFile, "a")
    file.write(f"{url},{scanId},{update}\n")
    file.close()
    print(f"{url} \t{scanId} \t{update}")
    
def launchDAST(url, appId, presenceId=None):
    scanName = "Log4Shell "+url
    if(len(scanName)>1024):
        scanName = scanName[:1024]
    options = {
        "ScanType": "Production",
        "PresenceId": presenceId,
        "StartingUrl": url,
        "TestOptimizationLevel": "Fastest",
        "ScanName": scanName,
        "AppId": appId,
    }
    scanId = asoc.createDastScan(options)
    return scanId

#Init the Output file if not already
if(not os.path.exists(OUTPUT_FILE_PATH)):
    print("Init the output file")
    with open(OUTPUT_FILE_PATH,"w+") as outputFile:
        outputFile.write("URL, SCAN_ID, LAST_UPDATE\n")

asoc = ASoC(API_KEY)
if(not asoc.login()):
    print("Failed to login to ASoC")
    sys.exit(1)
print("Logged Into ASoC")

print("Reading Input File")

#Read the input file for the URLS
with open(INPUT_FILE_PATH) as inputFile:
    for line in inputFile:
        if(not asoc.checkAuth()):
            print("Session Expired, logging in again")
            asoc.login()
        url = line.strip()
        if(checkScannedAlready(OUTPUT_FILE_PATH, url)):
            print(f"Already scanned {url}, skipping")
            continue
        scanId = launchDAST(url, ASOC_APP_ID, PRESENCE_ID)
        if(scanId):
            writeStatus(OUTPUT_FILE_PATH, url, scanId, asoc.getTimeStamp())
        else:
            print(f"An error occured creating the scan for {url}")
            print("Exiting")
            sys.exit(1)

if asoc.logout():
    print("Logged out of ASoC")
print("Done")