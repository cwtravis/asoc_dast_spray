import requests
import time
import datetime
import json

class ASoC:
    def __init__(self, apikey):
        self.apikey = apikey
        self.token = ""
    
    def login(self):
        resp = requests.post("https://cloud.appscan.com/api/V2/Account/ApiKeyLogin", json=self.apikey)
        if(resp.status_code == 200):
            jsonObj = resp.json()
            self.token = jsonObj["Token"]
            return True
        else:
            return False
        
    def logout(self):
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer "+self.token
        }
        resp = requests.get("https://cloud.appscan.com/api/V2/Account/Logout", headers=headers)
        if(resp.status_code == 200):
            self.token = ""
            return True
        else:
            return False
        
    def checkAuth(self):
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer "+self.token
        }
        resp = requests.get("https://cloud.appscan.com/api/V2/Account/TenantInfo", headers=headers)
        return resp.status_code == 200
    

    def createDastScan(self, options):
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer "+self.token
        }
        resp = requests.post("https://cloud.appscan.com/api/v2/Scans/DynamicAnalyzer", headers=headers, json=options)
        if(resp.status_code==201):
            jsonObj = resp.json()
            #print(json.dumps(jsonObj, indent=2))
            return jsonObj["Id"]
        print(resp.text)
        return None

    #Get current system timestamp
    def getTimeStamp(self):
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')