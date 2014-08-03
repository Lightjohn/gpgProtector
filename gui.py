#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import gpgp
import os, shutil

from PyQt4 import QtGui,QtCore


class Example(QtGui.QWidget):
    core = gpgp.gpgj()
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
        ligne1y = 30
        ligne2y = 100
        ligne3y = 170

        self.strinput = QtGui.QLabel(self)
        self.strinput.setObjectName("Dossier source")
        self.strinput.setText("Dossier source") 
        self.strinput.move(20,ligne1y)
        
        self.le1 = QtGui.QLineEdit(self)
        self.le1.setObjectName("Input")
        self.le1.setText("/Users/john/Desktop/testgpg")
        self.le1.move(200,ligne1y)
        
        self.cd1 = QtGui.QPushButton(self)
        self.cd1.setText("Choix dossier")
        self.cd1.move(400,ligne1y)
        self.cd1.clicked.connect(self.choose_pathin)
        
        self.strinput_summary = QtGui.QLabel(self)
        self.strinput_summary.setObjectName("Dossier source")
        self.strinput_summary.setText("Dossier source: Non definis                                                                                ") 
        self.strinput_summary.move(20,ligne1y+40)
        
        self.stroutput = QtGui.QLabel(self)
        self.stroutput.setObjectName("Dossier cible")
        self.stroutput.setText("Dossier cible") 
        self.stroutput.move(20,ligne2y)
        
        self.le2 = QtGui.QLineEdit(self)
        self.le2.setObjectName("Output")
        self.le2.setText("/Users/john/Desktop/testgpgout")
        self.le2.move(200,ligne2y)
        
        self.cd2 = QtGui.QPushButton(self)
        self.cd2.setText("Choix dossier")
        self.cd2.move(400,ligne2y)
        self.cd2.clicked.connect(self.choose_pathout)
        
        self.stroutput_summary = QtGui.QLabel(self)
        self.stroutput_summary.setObjectName("Dossier cible")
        self.stroutput_summary.setText("Dossier cible: Non definis                                                                                ") 
        self.stroutput_summary.move(20,ligne2y+40)
    
        self.btn = QtGui.QPushButton('Chiffrer', self)
        self.btn.move(10, ligne3y)
        self.btn.clicked.connect(self.Crypt)
        
        self.btn1 = QtGui.QPushButton('Dechiffrer', self)
        self.btn1.move(100, ligne3y)
        self.btn1.clicked.connect(self.Decrypt)
        
        self.btn2 = QtGui.QPushButton('Reset', self)
        self.btn2.move(200, ligne3y)
        self.btn2.clicked.connect(self.Reset)
        
        self.strerror = QtGui.QLabel(self)
        self.strerror.setText("                               ") 
        self.strerror.move(20,ligne3y+40)
        self.palette = QtGui.QPalette()
        self.palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
        self.strerror.setPalette(self.palette)
        
        self.setGeometry(0, 0, 550, 300)
        self.setWindowTitle('Chiffreur')
        self.show()
                    
    def Crypt(self):
        inputa = self.le1.text()
        self.strinput_summary.setText(inputa)
        outputa = self.le2.text()
        self.stroutput_summary.setText(outputa)
        self.print_good("chiffrage en cours")
        self.core.CRYPT(str(inputa), str(outputa))
        self.print_good("chiffrage termine")
            
    def Decrypt(self):
        inputa = self.le1.text()
        self.strinput_summary.setText(inputa)
        outputa = self.le2.text()
        self.stroutput_summary.setText(outputa)
        self.print_good("dechiffrage en cours")
        self.core.DECRYPT(str(outputa), str(inputa))
        self.print_good("dechiffrage termine")
    
    def Reset(self):
        shutil.rmtree(str(self.le2.text()))
        os.mkdir(str(self.le2.text()))
        self.print_good("RESET effectue")
    
    def choose_pathin(self):
        filename = QtGui.QFileDialog.getExistingDirectory(self, 'Open File', '/Users/john/Desktop', QtGui.QFileDialog.ShowDirsOnly)
        self.le1.setText(filename)
        self.strinput_summary.setText(filename)
        
    def choose_pathout(self):
        filename = QtGui.QFileDialog.getExistingDirectory(self, 'Open File', '/Users/john/Desktop', QtGui.QFileDialog.ShowDirsOnly)
        self.le2.setText(filename)
        self.stroutput_summary.setText(filename)
        
    def print_good(self, message):
        self.palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.darkGreen)
        self.strerror.setPalette(self.palette)
        self.strerror.setText(message)
        
    def print_bad(self,message):
        self.strerror.setText(message)
        self.palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
        self.strerror.setPalette(self.palette)



def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
