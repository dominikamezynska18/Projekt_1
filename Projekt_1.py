        # -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:32:34 2019

@author: Dominika
"""
import sys

from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QWidget, QApplication, QGridLayout, QColorDialog, QMessageBox,QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class AppWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Przecięcie odcinków"
        self.initInterface()
        self.initWidgets()

    def initInterface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 600, 600)
        self.show()

    def initWidgets(self):
        btn = QPushButton("Rysuj", self)
        btnClr = QPushButton("Wyczyść dane", self)
        btnSave = QPushButton("Zapisz do pliku", self)
        btnCol = QPushButton("Zmień kolor", self)
        xaLabel = QLabel("Xa", self)
        yaLabel = QLabel("Ya", self)
        xbLabel = QLabel("Xb", self)
        ybLabel = QLabel("Yb", self)
        xcLabel = QLabel("Xc", self)
        ycLabel = QLabel("Yc", self)
        xdLabel = QLabel("Xd", self)
        ydLabel = QLabel("Yd", self)
        xpLabel = QLabel("Xp", self)
        ypLabel = QLabel("Yp", self)
        self.xaEdit = QLineEdit("")
        self.yaEdit = QLineEdit("")
        self.xbEdit = QLineEdit("")
        self.ybEdit = QLineEdit("")
        self.xcEdit = QLineEdit("")
        self.ycEdit = QLineEdit("")
        self.xdEdit = QLineEdit("")
        self.ydEdit = QLineEdit("")
        self.xpEdit = QLineEdit("")
        self.xpEdit.setReadOnly( True )
        self.ypEdit = QLineEdit("")
        self.ypEdit.setReadOnly( True )


        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        #wywietlanie
        grid = QGridLayout()
        grid.addWidget(xaLabel, 1, 0)
        grid.addWidget(self.xaEdit, 1, 1)
        grid.addWidget(yaLabel, 2, 0)
        grid.addWidget(self.yaEdit, 2, 1)
        grid.addWidget(xbLabel, 3, 0)
        grid.addWidget(self.xbEdit, 3, 1)
        grid.addWidget(ybLabel, 4, 0)
        grid.addWidget(self.ybEdit, 4, 1)
        grid.addWidget(xcLabel, 5, 0)
        grid.addWidget(self.xcEdit, 5, 1)
        grid.addWidget(ycLabel, 6, 0)
        grid.addWidget(self.ycEdit, 6, 1)
        grid.addWidget(xdLabel, 7, 0)
        grid.addWidget(self.xdEdit, 7, 1)
        grid.addWidget(ydLabel, 8, 0)
        grid.addWidget(self.ydEdit, 8, 1)
        grid.addWidget(btn, 9, 0, 1, 2)
        grid.addWidget(btnCol, 10, 0, 1, 2)
        grid.addWidget(btnClr, 11, 0, 1, 2)
        grid.addWidget(btnSave, 12, 0, 1, 2)
        grid.addWidget(xpLabel, 13, 0)
        grid.addWidget(self.xpEdit, 13,1)
        grid.addWidget(ypLabel, 14, 0)
        grid.addWidget(self.ypEdit, 14,1)
        self.setLayout(grid)
        grid.addWidget(self.canvas, 1, 2, -1, -1)

        btn.clicked.connect(self.oblicz)
        btnCol.clicked.connect(self.zmienKolor)
        btnClr.clicked.connect(self.wyczysc)
        btnSave.clicked.connect(self.save)

    def zmienKolor(self):
        kolor = QColorDialog.getColor()
        if kolor.isValid():
            print(kolor.name())
            self.rysuj(kol=kolor.name())

    def sprawdzLiczbe(self, element):
        if element.text().lstrip('-').replace('.','',1).isdigit():
            return float(element.text())
        else:
            element.setFocus()
            return None

    def wyczysc(self):
        self.xaEdit.clear()
        self.yaEdit.clear()
        self.xbEdit.clear()
        self.ybEdit.clear()
        self.xcEdit.clear()
        self.ycEdit.clear()
        self.xdEdit.clear()
        self.ydEdit.clear()
        self.figure.clear()
        self.ax.cla()
        self.canvas.draw()

    def save(self):
        filename = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)")

        file = open(filename[0],'w')
        Xpr= round(Xp,3)
        Ypr= round(Yp,3)
        text = "Xp: " + str(Xpr) + "\n" + "Yp: " + str(Ypr)
        file.write(text)
        file.close()
        if filename:
            print(filename)


    def oblicz(self):
        global Xp
        global Yp
        xa = self.sprawdzLiczbe(self.xaEdit)
        ya = self.sprawdzLiczbe(self.yaEdit)
        xb = self.sprawdzLiczbe(self.xbEdit)
        yb = self.sprawdzLiczbe(self.ybEdit)
        xc = self.sprawdzLiczbe(self.xcEdit)
        yc = self.sprawdzLiczbe(self.ycEdit)
        xd = self.sprawdzLiczbe(self.xdEdit)
        yd = self.sprawdzLiczbe(self.ydEdit)

        dXab= xb-xa
        dXac= xc-xa
        dXcd= xd-xc
        dYab= yb-ya
        dYac= yc-ya
        dYcd= yd-yc
        print(dXab,dXac,dXcd,dYab,dYac,dYcd)

        if ((dXab*dYcd) - (dYab*dXcd))==0:
                print("Niepoprawne dane lub brak rozwiązania")
                QMessageBox.about(self, "Błąd", "Niepoprawne dane lub brak rozwiązania")

        else:
                t1= ((dXac*dYcd) - (dYac*dXcd))/((dXab*dYcd) - (dYab*dXcd))
                t2= ((dXac*dYab) - (dYac*dXab))/((dXab*dYcd) - (dYab*dXcd))

                li1 = dXac*dYcd-dYac*dXcd
                li2 = dXac*dYab-dYac*dXab
                mian = dXab*dYcd-dYab*dXcd
                Xp = xa + (t1*dXab)
                Yp = ya + (t1*dYab)
                if mian!=0:
                    t1=li1/mian
                    t2=li2/mian
                    if 0<=t1<=1 and 0<=t2<=1:
                        Xp = xa + (t1*dXab)
                        Yp = ya + (t1*dYab)
                        print ('Xp =', Xp)
                        print ('Yp =', Yp)
                        print('Odcinki przecinają się')
                        #QMessageBox.about(self, "Info", "Odcinki przecinają się")

                    elif 0<=t1<=1 or 0<=t2<=1:
                        Xp = xa + (t1*dXab)
                        Yp = ya + (t1*dYab)
                        print ('Xp =', Xp)
                        print ('Yp =', Yp)
                        print ('Przedłużenie jednego odcinka przecina drugi odcinek')
                        self.mode=2
                    else:
                        Xp = xa + (t1*dXab)
                        Yp = ya + (t1*dYab)
                        print ('Xp =', Xp)
                        print ('Yp =', Yp)
                        print ('Przecinają się przedłużenia odcinków')
                        self.mode=2


                elif mian==0:
                    print("Proste równoległe, brak rozwiązania")

                self.rysuj()

    def rysuj(self, kol="red"):

        xa = self.sprawdzLiczbe(self.xaEdit)
        ya = self.sprawdzLiczbe(self.yaEdit)
        xb = self.sprawdzLiczbe(self.xbEdit)
        yb = self.sprawdzLiczbe(self.ybEdit)
        xc = self.sprawdzLiczbe(self.xcEdit)
        yc = self.sprawdzLiczbe(self.ycEdit)
        xd = self.sprawdzLiczbe(self.xdEdit)
        yd = self.sprawdzLiczbe(self.ydEdit)

        print(xa,ya,xb,yb,xc,yc,xd,yd)
        if None is not [xa,ya,xb,yb,xc,yc,xd,yd]:#if (x is not None) and (y is not None):
            xa = float(self.xaEdit.text())
            ya = float(self.yaEdit.text())
            xb = float(self.xbEdit.text())
            yb = float(self.ybEdit.text())
            xc = float(self.xcEdit.text())
            yc = float(self.ycEdit.text())
            xd = float(self.xdEdit.text())
            yd = float(self.ydEdit.text())
        0
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(xa, ya, color='blue', marker='o')
        self.ax.text(xa,ya, "A("+str(xa)+","+str(ya)+")", color="black")
        self.ax.plot(xb, yb, color='red', marker='o')
        self.ax.text(xb, yb, "B("+str(xb)+","+str(yb)+")", color='black')
        self.ax.plot(xc, yc, color='green', marker='o')
        self.ax.text(xc,yc, "C("+str(xc)+","+str(yc)+")", color="black")
        self.ax.plot(xd, yd, color='orange', marker='o')
        self.ax.text(xd,yd, "D("+str(xd)+","+str(yd)+")", color="black")
        self.ax.plot(Xp,Yp, color='brown', marker='o')
        self.ax.text(Xp,Yp, "P("+str(round(Xp,2))+","+str(round(Yp,2))+")", color="black")
        #if self.mode == 2:
        Xpa=[xa,Xp]
        Xpc=[xc,Xp]
        Ypa=[ya,Yp]
        Ypc=[yc,Yp]
        self.ax.plot(Xpa,Ypa, color="black", linestyle="--")
        self.ax.plot(Xpc,Ypc, color="black", linestyle="--")
        Xab=[xa,xb]
        Yab=[ya,yb]
        Xcd=[xc,xd]
        Ycd=[yc,yd]
        self.ax.plot(Xcd,Ycd,color=kol )
        self.ax.plot(Xab,Yab, color=kol )


        self.canvas.draw()
        self.xpEdit.setText(str(Xp))
        self.ypEdit.setText(str(Yp))

        #self.xEdit.setText("1")

def main():

    app = QApplication(sys.argv)
    window = AppWindow()
    app.exec_()

if __name__ == '__main__':
    main()
