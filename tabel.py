import sys
import io
import pandas as pd
import folium # pip install folium

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 500
        self.initUI()
    
    @pyqtSlot()
    def keluar(self):
        QCoreApplication.quit()

    def initUI(self):
        menubar = QMenuBar()
        actionFile = menubar.addMenu("File")
        actionFile.addAction("Input Data")
        actionFile.addAction("Import Data")
        actionFile.addSeparator()
        actionFile.addAction("Keluar", self.keluar)
        menubar.addMenu("About")
        
        coordinate = (-0.789275, 113.921327)
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=4,
            location=coordinate
        )
        
        data = pd.DataFrame({
           'lat':[-0.12678333422024976, -2.0860752969863787],
           'lon':[113.45099842083398, 103.80901401544466],
        }, dtype=str)

        for i in range(0,len(data)):
            folium.Circle(location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
                  radius=500, 
                  fill=True, 
                  fill_color="red",
                  color="red",
                  fill_opacity=1
                  ).add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        btn = QPushButton('ok')

        webView.setHtml(data.getvalue().decode())
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()
        self.layout = QGridLayout()
        self.setLayout(self.layout) 
        self.layout.addWidget(menubar, 0, 0, 1, 5)
        self.layout.addWidget(webView, 1, 0, 4, 5)
        self.layout.addWidget(self.tableWidget, 5, 0, 1, 3) 
        self.layout.addWidget(btn, 5, 3, 1, 1)

        # Show widget
        self.show()

    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Cell (1,2)"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Cell (2,1)"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Cell (2,2)"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Cell (4,2)"))
        self.tableWidget.move(0,0)

        # table selection change
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())  