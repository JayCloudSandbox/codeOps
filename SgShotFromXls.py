import sys,os
import openpyxl
import shotgun_api3

class ShotGridCreate():
    def __init__(self,serverPth,scNm,scKey,prjId,seq,shot,taskTemplate,Type,shDesc):
        self.serverPath = serverPth
        self.scriptName = scNm
        self.scriptKey = scKey
        self.projectId = prjId
        self.seq = seq
        self.shotCode = shot
        self.taskTemplate = taskTemplate
        self.Type = Type
        self.shotDescription = shDesc

    def grabData(self):
        wb = openpyxl.load_workbook('C://Book.xlsx')
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
        
    def runShotCreate(self):
        SERVER_PATH = self.serverPath
        SCRIPT_NAME  = self.scriptName
        SCRIPT_KEY = self.scriptKey
        studentCount,firstName,lastName = self.grabData()
        prjId = int(self.projectId)
        tskTemplt = self.taskTemplate
        desc = self.shotDescription
        sequenceName = self.seq
        shot = self.shotCode
        type = self.Type
        sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

        filters = [['code', 'is', tskTemplt]]
        template = sg.find_one('TaskTemplate', filters)

        filters = [['code', 'is', sequenceName]]
        sequence = sg.find_one('Sequence', filters)

        print("\nstarted creating shots ")

        for count in range(int(studentCount)):
            print("craeted {}-{}-{} ".format(count,shot,firstName[count]))
            data = {
                "project": {"type": "Project", "id": prjId},
                "sg_sequence": sequence,
                "code": shot+"-{}".format(firstName[count]),
                "task_template": template,
                "sg_shot_type": str(type),
                "description": desc,
            }
            sg.create('Shot', data)

        print("\ncompleted creating shots")

if __name__ == '__main__':
    ShotGridCreate("https://shotgrid.autodesk.com/","test_create_shot","Thnctx1@djvczmqbiq",716,"RT_T001","RT_S001_T001","Film VFX - Full CG Shot w/ Character","VFX","shot automate frol xls").runShotCreate()
