import sys,os
import openpyxl
import shotgun_api3

class SeqGridCreate():
    def __init__(self,serverPth,scNm,scKey,prjId,seq):
        self.serverPath = serverPth
        self.scriptName = scNm
        self.scriptKey = scKey
        self.projectId = prjId
        self.seqCode = seq
            
    def runSeqCreate(self):
        SERVER_PATH = self.serverPath
        SCRIPT_NAME  = self.scriptName
        SCRIPT_KEY = self.scriptKey
        prjId = int(self.projectId)
        seq = self.seqCode
        sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

        print("\nstarted creating assets ")
        print("craeted {} ".format(seq))

        data = {
            "project": {"type": "Project", "id": prjId},
            "code": seq,
        }
        sg.create('Sequence', data)

        print("\ncompleted creating assets")

if __name__ == '__main__':
    SeqGridCreate("https:some.shotgrid.autodesk.com/","test_create_shot","Thnctx1@dcjvczmqbiq",716,"RT_T001").runSeqCreate()
