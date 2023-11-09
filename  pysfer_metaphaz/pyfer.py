import json
import os
import logging


def localvar():
    return localvars

    
class localvars:
    def __init__(self):
        self.folder = os.path.dirname(os.path.realpath(__file__))+"/.pyfer"
        self.file = os.path.dirname(os.path.realpath(__file__))+"/.pyfer/pyferlocaldata.json"
        if os.path.exists(self.folder):
            open(self.file,"w").write("{}")
        else:
            os.makedirs(self.folder)
            
        logging.basicConfig(filename=f"{self.folder}+/locallogs.log",level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    def get(self ,var_name: str):
        localjsondata = json.loads(open(self.file,"r").read())
        if var_name in localjsondata:
            return localjsondata[var_name]
        else:
            logging.warning("Unable to get "+var_name)
            return
        
    def update(self, var_name: str, value):
        localjsondata = json.loads(open(self.file,"r").read())
        localjsondata[var_name] = value
        open(self.file,"w").write(json.dumps(localjsondata))
        return self
    
    def delete(self, var_name: str):
        localjsondata = json.loads(open(self.file,"r").read())
        del localjsondata[var_name] 
        open(self.file, "w").write(json.dumps(localjsondata))
    
    def replace(self, old_name: str, new_name: str):
        localjsondata = json.loads(open(self.file,"r").read())
        if old_name in localjsondata:
            value = localjsondata[old_name]
            del localjsondata[old_name]
            localjsondata[new_name] = value
            open(self.file,"w").write(json.dumps(localjsondata))
        else:
            logging.warning("There is no "+old_name+" in cache")
            return

    def getjson(self):
        localjsondata = json.loads(open(self.file,"r").read())
        return localjsondata
    
    def updatejson(self, json_type):
        open(self.file,"w").write(json.dumps(json_type))
        return self
    
    def deletejson(self):
        open(self.file,"w").write("{}")








