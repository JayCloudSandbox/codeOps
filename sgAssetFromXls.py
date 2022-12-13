import sys,os
import openpyxl
import shotgun_api3

class AssetGridCreate():
    def __init__(self,serverPth,scNm,scKey,prjId,asset,taskTemplate,assetType,shDesc):
        self.serverPath = serverPth
        self.scriptName = scNm
        self.scriptKey = scKey
        self.projectId = prjId
        self.assetCode = asset
        self.taskTemplate = taskTemplate
        self.assetType = assetType
        self.shotDescription = shDesc

    def grabData(self):
        wb = openpyxl.load_workbook('C:Downloads//Book.xlsx')
        sheet = wb.active
        i=0
        FirstName = []
        LastName = []
        # B=firstname
        # C=lastname
        # D=email
        # E=location
        # F=ip
        # G=project
        # H=timezone
        # J=server
        for colA in sheet['B']:
            if not colA.value == "First Name":
                if not colA.value:
                    continue
                else:
                    FirstName.append(colA.value)
                    i+=1
        for colB in sheet['C']:
            if not colB.value == "Last Name":
                if not colB.value:
                    continue
                else:
                    LastName.append(colB.value)
    
        return i,FirstName,LastName
        
    def runAssetCreate(self):
        SERVER_PATH = self.serverPath
        SCRIPT_NAME  = self.scriptName
        SCRIPT_KEY = self.scriptKey
        studentCount,firstName,lastName = self.grabData()
        prjId = int(self.projectId)
        tskTemplt = self.taskTemplate
        desc = self.shotDescription
        asst = self.assetCode
        assType = self.assetType
        sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

        filters = [['code', 'is', tskTemplt]]
        template = sg.find_one('TaskTemplate', filters)
        print("\nstarted creating assets ")

        for count in range(int(studentCount)):
            print("craeted {}-{}-{} ".format(count,asst,firstName[count]))
            data = {
                "project": {"type": "Project", "id": prjId},
                "code": asst+"-{}".format(firstName[count]),
                "task_template": template,
                "sg_asset_type": str(assType),
                "description": desc,
            }
            sg.create('Asset', data)

        print("\ncompleted creating assets")

if __name__ == '__main__':
    AssetGridCreate("https://some.com/","test_create_shot","Thnctx1@dpykiddcjvczmq",716,"charRobot","Film VFX - Character Asset","Character","asset automate frol xls").runAssetCreate()
