import sys
import io
import pandas as pd
import folium # pip install folium
import csv

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import *

import sqlite3

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'BMKG'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 700
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.cMenuBar()
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()
        # self.insertData();
        # 
    # def insertData(self):
    #     # Create table
    #     con = sqlite3.connect('main.db')
    #     cur = con.cursor()
    #     # Insert a row of data
        
    #     cur.execute("INSERT INTO kordinat (tgl_wib, tgl_wita, tgl_wit, lintang, bujur, kedalaman, magnitude, sumber, keterangna, wil, dir) VALUES ('xs','putra',3,3,3,3,3,3,3,3,3) ")
        
    #     # Save (commit) the changes
    #     con.commit()

    def cMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction("Input Data")
        fileMenu.addAction("Import Data")
        fileMenu.addSeparator()
        fileMenu.addAction("Keluar", self.keluar)

        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")

    @pyqtSlot()
    def keluar(self):
        QCoreApplication.quit()
    
class MyTableWidget(QWidget):
    def __init__(self, parent):
        self.matrixCol = 0
        self.matrixRow = 0
        self.pathFileCsv = ''

        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300,200)
        # Add tabs
        self.tabs.addTab(self.tab1,"Dashboard")
        self.tabs.addTab(self.tab2,"List Data")
        self.tabs.addTab(self.tab3,"Import Data")
        # self.tabs.setStyleSheet("font-size:15px")
        

        # Create 2 tab
        self.createTable()
        self.tab2.layout = QGridLayout(self)
        
        self.hapusData = QPushButton("Hapus Data Terpilih")
        self.hapusData.setStyleSheet("""
                QPushButton{
                    background-color:#ff4d4d; padding:6px; color: black; border-radius:3px;
                }
                QPushButton:hover{
                    background-color:#ff9999
                }
            """)
        self.loadData = QPushButton("Load Data")
        self.loadData.setStyleSheet("""
                QPushButton{
                    background-color:#1a8cff; padding:6px; color: white; border-radius:3px;
                }
                QPushButton:hover{
                    background-color:#80bfff
                }
            """)
        
        simpan = QPushButton("SIMPAN")
        simpan.clicked.connect(self.simpanData)
        simpan.setStyleSheet("""
                QPushButton{
                    background-color:#1a8cff; padding:6px; color: white; border-radius:3px;
                }
                QPushButton:hover{
                    background-color:#80bfff
                }
            """)
        self.loadData.clicked.connect(self.loadDataKordinat)

        titleForm = QLabel('Masukan Data Manual')
        titleForm.setFont(QFont('Arial', 15))
        
        lwib = QLabel('WIB')
        lwita = QLabel('WITA')
        lwit = QLabel('WIT')
        llintang = QLabel('LINTANG')

        lbujur = QLabel('BUJUR')
        lkedalaman = QLabel('KEDALAMAN')
        lmagnitude = QLabel('MAGNITUDE')
        lsumber = QLabel('SUMBER')

        lketerangan = QLabel('KETERANGAN')
        lwil = QLabel('WIL')
        ldir = QLabel('DIR')

        self.tglwib = QLineEdit(placeholderText = "Tanggal WIB, format 01-12-2021 12:00:21")
        self.tglwib.setGeometry(QtCore.QRect(50, 70, 171, 31))
        self.tglwita = QLineEdit(placeholderText = "Tanggal WITA, format 01-12-2021 12:00:21")
        self.tglwit = QLineEdit(placeholderText = "Tanggal WIB, format 01-12-2021 12:00:21")
        self.lintang = QLineEdit(placeholderText = "Masukan Lintang")

        self.bujur = QLineEdit(placeholderText = "Masukan Bujur")
        self.kedalaman = QLineEdit(placeholderText = "Masukan kedalaman")
        self.magnitude = QLineEdit(placeholderText = "Masukan magnitude")
        self.sumber = QLineEdit(placeholderText = "Masukan sumber")

        self.ket = QLineEdit(placeholderText = "Masukan disini")
        self.wil = QLineEdit(placeholderText = "Masukan disini")
        self.dirr = QLineEdit(placeholderText = "Masukan disini")

        self.hapusData.clicked.connect(self.hapusDataFromDb)
        
        self.tab2.layout.addWidget(self.tableWidget, 0, 0, 20, 5)
        self.tab2.layout.addWidget(titleForm, 21, 0, 1, 1)
        self.tab2.layout.addWidget(lwib, 22, 0, 1, 1)
        self.tab2.layout.addWidget(self.tglwib, 24, 0, 1, 1)

        self.tab2.layout.addWidget(lwita, 22, 2, 1, 1)
        self.tab2.layout.addWidget(self.tglwita, 24, 2, 1, 1)

        self.tab2.layout.addWidget(lwit, 22, 3, 1, 1)
        self.tab2.layout.addWidget(self.tglwit, 24, 3, 1, 1)

        self.tab2.layout.addWidget(llintang, 22, 4, 1, 1)
        self.tab2.layout.addWidget(self.lintang, 24, 4, 1, 1)

        # baris 2 form
        self.tab2.layout.addWidget(lbujur, 25, 0, 1, 1)
        self.tab2.layout.addWidget(self.bujur, 27, 0, 1, 1)

        self.tab2.layout.addWidget(lkedalaman, 25, 2, 1, 1)
        self.tab2.layout.addWidget(self.kedalaman, 27, 2, 1, 1)

        self.tab2.layout.addWidget(lmagnitude, 25, 3, 1, 1)
        self.tab2.layout.addWidget(self.magnitude, 27, 3, 1, 1)

        self.tab2.layout.addWidget(lsumber, 25, 4, 1, 1)
        self.tab2.layout.addWidget(self.sumber, 27, 4, 1, 1)

        # baris 3 form
        self.tab2.layout.addWidget(lketerangan, 28, 0, 1, 1)
        self.tab2.layout.addWidget(self.ket, 30, 0, 1, 1)

        self.tab2.layout.addWidget(lwil, 28, 2, 1, 1)
        self.tab2.layout.addWidget(self.wil, 30, 2, 1, 1)

        self.tab2.layout.addWidget(ldir, 28, 3, 1, 1)
        self.tab2.layout.addWidget(self.dirr, 30, 3, 1, 1)
 

        self.tab2.layout.addWidget(simpan, 31, 0, 1, 5)
        self.tab2.layout.addWidget(self.hapusData, 0, 5, 1, 1, alignment=Qt.AlignTop)
        self.tab2.layout.addWidget(self.loadData, 1, 5, 1, 1, alignment=Qt.AlignTop)
        self.tab2.setLayout(self.tab2.layout)
        
        # Create second tab
        coordinate = (-0.789275, 113.921327)
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=5,
            location=coordinate
        )
        
        data = pd.DataFrame({
           'lat':[-6.931761333013024, -6.9344452298036705, -6.876089262836584],
           'lon':[107.67049155274123, 107.65680155798631, 107.8216913262112],
           'sizeDot':[10, 100, 210],
           'colorDot':['red', 'green', 'yellow'],
        }, dtype=str)

        for i in range(0,len(data)):
            folium.Circle(location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
                  radius=data.iloc[i]['sizeDot'], 
                  fill=True, 
                  fill_color=data.iloc[i]['colorDot'],
                  color=data.iloc[i]['colorDot'],
                  fill_opacity=1
                  ).add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        # self.createTable()
        
        # add image
        self.gambarTabelKedalaman()

        webView.setHtml(data.getvalue().decode())
        self.tab1.layout = QGridLayout(self)
        self.tab1.layout.addWidget(webView, 0, 0, 4, 5)
        self.tab1.layout.addWidget(self.label, 5, 0, 1, 3)
        self.tab1.setLayout(self.tab1.layout)
        
        # tab 3
        btnBrowse = QPushButton('Browse')
        btnBrowse.clicked.connect(self.openFileNameDialog)       
        btnBrowse.setStyleSheet('height:30px;background-color:aqua')
        submitBtnBrowse = QPushButton('Import Sekarang..')
        submitBtnBrowse.clicked.connect(self.importData)

        submitBtnBrowse.setStyleSheet('background-color:#1a8cff')
        lrule = QLabel('Ketentuan File .CSV yang bisa digunakan')
        self.lbrowse = QLabel('Browse File (.csv)')
        self.lbrowse.setStyleSheet("background-color:aqua")

        lrule.setStyleSheet("font-size:20px")

        self.tab3.layout = QGridLayout(self)
        self.tab3.layout.addWidget(self.lbrowse, 0, 0)
        self.tab3.layout.addWidget(btnBrowse, 0, 1, alignment=Qt.AlignTop)
        self.tab3.layout.addWidget(submitBtnBrowse, 1, 0, alignment=Qt.AlignTop)
        self.tab3.layout.addWidget(lrule, 5, 0, 1, 1)
        
        self.tab3.layout.addWidget(self.listRule(), 7, 0, 10, 1)
        self.tab3.setLayout(self.tab3.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        # self.importData()

    def listRule(self):
        listWidget = QListWidget()
        QListWidgetItem("1. File Harus .CSV", listWidget)
        QListWidgetItem("2. Urutan Kolom HARUS berurutan -> Tanggal WIB, Tanggal WITA, Tanggal WIT etc", listWidget)
        QListWidgetItem("3. Disarankan Setiap Import data tidak lebih dari 100", listWidget)
        listWidget.setStyleSheet("border:none")
        return listWidget

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV (*.csv)", options=options)
        if fileName:
            self.pathFileCsv = fileName
        self.lbrowse.setText("Lokasi file = {0}".format(fileName))

    def reloadTable(self):
        self.createTable()
        lloadin = QLabel('Loading...')
        self.tab2.layout.addWidget(lloadin, 0, 0, 20, 5)
        self.tab2.layout.addWidget(self.tableWidget, 0, 0, 20, 5)

    def loadDataKordinat(self):
        self.reloadTable()

    def gambarTabelKedalaman(self):
        # add img
        self.label = QLabel(self)
        # loading image
        self.pixmap = QPixmap('aa.JPG')

        # adding image to label
        self.label.setPixmap(self.pixmap)
 
        # Optional, resize label to image size
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())
    
    @pyqtSlot()
    def importData(self):
        if self.pathFileCsv == '':
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Pastikan File .CSV sudah dipilih !")
            msgBox.setWindowTitle("Oppss")
            msgBox.setStandardButtons(QMessageBox.Ok)
            # msgBox.buttonClicked.connect(msgButtonClick)
            returnValue = msgBox.exec()
        else:
            num = 0;
            with open(self.pathFileCsv, newline='') as csvfile:
                spamreader = csv.reader(csvfile)
                for row in spamreader:
                    if num >= 1:
                        ctglwib = row[0]
                        ctglwita = row[1]
                        ctglwit = row[2]
                        con = sqlite3.connect('main.db')
                        cur = con.cursor()
                        cur.execute("insert into kordinat (tgl_wib, tgl_wita, tgl_wit) values ('{0}', '{1}', '{2}' )".format(ctglwib,ctglwita, ctglwit))
                        con.commit()
                    num +=1
            self.reloadTable()
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Proses Import selesai !!")
            msgBox.setWindowTitle("Informasi")
            msgBox.setStandardButtons(QMessageBox.Ok)
            # msgBox.buttonClicked.connect(msgButtonClick)
            returnValue = msgBox.exec()
            self.pathFileCsv = ''
            self.lbrowse.setText("Browse File (.CSV)")
            


    @pyqtSlot()
    def simpanData(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Yakin untuk mengimpan data ini ?")
        msgBox.setWindowTitle("Menyimpan Data")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # msgBox.buttonClicked.connect(msgButtonClick)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            
            con = sqlite3.connect('main.db')
            cur = con.cursor()
            cur.execute(" INSERT INTO kordinat (tgl_wib, tgl_wita, tgl_wit, lintang, bujur, kedalaman, magnitude, sumber, keterangna, wil, dir) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}') ".format(self.tglwib.text(), self.tglwita.text(), self.tglwit.text(), self.lintang.text(), self.bujur.text(), self.kedalaman.text(), self.magnitude.text(), self.sumber.text(), self.ket.text(), self.wil.text(), self.dirr.text()))
            con.commit()
            self.reloadTable()

            self.tglwib.clear()
            self.tglwita.clear()
            self.tglwit.clear()
            self.lintang.clear()
            self.bujur.clear()
            self.kedalaman.clear()
            self.magnitude.clear()
            self.sumber.clear()
            self.ket.clear()
            self.wil.clear()
            self.dirr.clear()
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Data berhasil disimpan !")
            msgBox.setWindowTitle("Berhasil")
            msgBox.setStandardButtons(QMessageBox.Ok)
            # msgBox.buttonClicked.connect(msgButtonClick)
            returnValue = msgBox.exec()

    @pyqtSlot()
    def hapusDataFromDb(self):
        row = self.tableWidget.rowCount()
        if row >= 1:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("Yakin akan menghapus data ini ?")
            msgBox.setWindowTitle("Menghapus Data")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msgBox.buttonClicked.connect(msgButtonClick)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                data = []
                col = self.tableWidget.columnCount()
                for x in range(col):
                    data.append(self.tableWidget.item(self.matrixRow, x).text())

                con = sqlite3.connect('main.db')
                cur = con.cursor()
                cur.execute("delete from kordinat where tgl_wib='{0}' and tgl_wita='{1}' and tgl_wit='{2}' ".format(data[0], data[1], data[2]))
                con.commit()
                self.reloadTable()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Tidak ada data yang dihapus !")
            msgBox.setWindowTitle("Informasi")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    @pyqtSlot()
    def delRow(self):
        self.createTable()
        # button = self.sender()
        # if button:
        #     rownya = self.tableWidget.indexAt(button.pos()).row()
        #     # rownya = self.tableWidget.currentRow()
        #     self.tableWidget.removeRow(rownya)
        #     ix = self.tableWidget.model().index(
        #         rownya, self.tableWidget.currentColumn()
        #     )
        #     self.tableWidget.setCurrentIndex(ix)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def createTable(self):
        print("--------ctabel load")
        con = sqlite3.connect('main.db')
        cur = con.cursor()

        for row in cur.execute('SELECT count(*) jml FROM kordinat limit 200'):
            jmlData = row[0]

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(jmlData)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Tanggal WIB", "Tanggal WITA", "Tanggal WIT"])


        # self.tableWidget.setRowCount(4)
        tindex = 0
        for row in cur.execute('SELECT * FROM kordinat'):
            # deleteButton.clicked.connect(self.deleteClicked)
            # btn = QtWidgets.QPushButton("delete_this_row")
            # btn.clicked.connect(self.delRow)
            self.tableWidget.setItem(tindex,0, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tindex,1, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tindex,2, QtWidgets.QTableWidgetItem(row[3]))
            # self.tableWidget.setCellWidget(tindex, 3, btn)
            # print(tindex," - ", row[1]," - ", row[2]," - ", row[3])
            tindex+=1

        self.tableWidget.selectionModel().selectionChanged.connect(self.on_select)

    def on_select(self, selected, deselected):
        for ix in selected.indexes():
            self.matrixRow = ix.row()
            self.matrixCol = ix.column()
        # for ix in deselected.indexes():
        #     print('Deselected Cell Location Row: {0}, Column: {1}'.format(ix.row(), ix.column()))
        # print('-------')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    app.setStyleSheet('QLineEdit{padding: 6px;}')
    
    ex = App()
    sys.exit(app.exec_())