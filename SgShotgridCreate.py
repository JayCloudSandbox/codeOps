from PyQt6 import QtCore, uic, QtWidgets
from PyQt6.QtGui import QMovie, QPixmap
from PyQt6.QtWidgets import QMessageBox
import sys,os
import shotgun_api3


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        #super(MyWidget,self).__init__()
#       self.setFixedSize(681, 541)
        #ui_file = 'C:\\sgCreateShotsBgRez.ui'
        self.ui = uic.loadUi(ui_file,self)
        self.home()
        self.mb = QMessageBox()
        self.mb.about(self, "Default :", "To create a script in shotgun, at the top in user settigs drop down -> select script , create a script call it a name like Create Multiple Shots and copy the key it generates , you need this key to run to connect and run the script for shotgunStudio")

#       self.update_image()

        self.show()

    def home(self):
        self.gifPath = "C:\\fallinNum.gif"
        self.pButton = self.ui.pushButton
        self.pButton.clicked.connect(self.runShotCreate)
        self.serverPath = self.ui.serverPth
        self.scriptName = self.ui.scNm
        self.scriptKey = self.ui.scKey
        self.projectId = self.ui.prjId
        self.shotPrefix = self.ui.shPrfx
        self.shotStart = self.ui.shSt
        self.shotEnd = self.ui.shEn
        self.shotIncrement = self.ui.shInc
        self.shotDescription = self.ui.shDesc
        self.shotStatus = self.ui.shStat

        self.labelAnim = self.ui.labelAnimGif
        self.gif = QMovie(self.gifPath)
        self.labelAnim.setMovie(self.gif)
        self.labelAnim.setScaledContents(True)
        self.gif.start()

    def update_image(self):
        inSeqImg = self.labelGif
        self.gifseq = QMovie(inSeqImg)
        self.dspl.setMovie(self.gifseq)
        self.dspl.setScaledContents(True)
        self.gifseq.start()

    def createShotDescription(self):
        self.desc = str(self.shotDescription.toPlainText())
        return self.desc

    def createShotNumber(self,shotNum):
        self.shotInitial = int(self.shotPrefix.toPlainText())
        self.shotInc = int(self.shotIncrement.toPlainText())
        self.shotNum = shotNum

        self.shotNum = format(self.shotNum,"03")
        self.shotNum = str(self.shotInitial) + "_" + str(self.shotNum)
#       print("shot number is%s"%self.shotNum)
        return self.shotNum

    def createShotProgress(self):
        self.shotProgress = str(self.shotStatus.toPlainText())
        return self.shotProgress

    def runShotCreate(self):
        SERVER_PATH = self.serverPath.toPlainText()
        SCRIPT_NAME  = self.scriptName.toPlainText()
        SCRIPT_KEY = self.scriptKey.toPlainText()
        shotSt = int(self.shotStart.toPlainText())
        shotEn = int(self.shotEnd.toPlainText())
        prjId = int(self.projectId.toPlainText())
        shotStts = str(self.shotStatus.toPlainText())

        sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)
        if shotSt and shotEn:
            for shot in range(int(shotSt),int(shotEn)):
                if shot%10==0:
                    filter = [['code', 'is', str(shot)]]
                    if not sg.find_one('Shot', filter):
                        data = {
                            'project': {"type":"Project","id": prjId},
                            'code': '%s'%self.createShotNumber(shot),
                            'description': '%s'%self.createShotDescription(),
                            'sg_status_list': '%s'%self.createShotProgress()
                        }
                        sg.create('Shot', data)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MyWidget()
    w.setWindowTitle(" Shotgun Shots Creator ")
    app.exec()
