import sys
import io
import folium # pip install folium
import csv

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QPushButton, QMainWindow, QWidget, QApplication, QVBoxLayout, QTabWidget, QTableWidget, QGridLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox
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
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        # self.cMenuBar()
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

    # def cMenuBar(self):
        # menuBar = self.menuBar()
        # # Creating menus using a QMenu object
        # fileMenu = QMenu("&File", self)
        # menuBar.addMenu(fileMenu)
        # fileMenu.addAction("Input Data")
        # fileMenu.addAction("Import Data")
        # fileMenu.addSeparator()
        # fileMenu.addAction("Keluar", self.keluar)

        # editMenu = menuBar.addMenu("&Edit")
        # helpMenu = menuBar.addMenu("&Help")

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
        lwib.setStyleSheet("font-weight:bold")
        lwita = QLabel('WITA')
        lwita.setStyleSheet("font-weight:bold")
        lwit = QLabel('WIT')
        lwit.setStyleSheet("font-weight:bold")
        llintang = QLabel('LINTANG')
        llintang.setStyleSheet("font-weight:bold")

        lbujur = QLabel('BUJUR')
        lbujur.setStyleSheet("font-weight:bold")
        lkedalaman = QLabel('KEDALAMAN')
        lkedalaman.setStyleSheet("font-weight:bold")
        lmagnitude = QLabel('MAGNITUDO')
        lmagnitude.setStyleSheet("font-weight:bold")
        lsumber = QLabel('SUMBER')
        lsumber.setStyleSheet("font-weight:bold")

        lketerangan = QLabel('KETERANGAN')
        lketerangan.setStyleSheet("font-weight:bold")
        lwil = QLabel('WIL')
        lwil.setStyleSheet("font-weight:bold")
        ldir = QLabel('DIR')
        ldir.setStyleSheet("font-weight:bold")

        self.tglwib = QLineEdit(placeholderText = "Tanggal WIB, format 01-12-2021 12:00:21")
        self.tglwib.setGeometry(QtCore.QRect(50, 70, 171, 31))
        self.tglwita = QLineEdit(placeholderText = "Tanggal WITA, format 01-12-2021 12:00:21")
        self.tglwit = QLineEdit(placeholderText = "Tanggal WIB, format 01-12-2021 12:00:21")
        self.lintang = QLineEdit(placeholderText = "Masukan Lintang")

        self.bujur = QLineEdit(placeholderText = "Masukan Bujur")
        self.kedalaman = QLineEdit(placeholderText = "Masukan kedalaman")
        self.magnitude = QLineEdit(placeholderText = "Masukan magnitudo")
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
        
        # data = pd.DataFrame({
        #    'lat':[-6.931761333013024, -6.9344452298036705, -6.876089262836584, -6.918915950425016, -6.835597128916457, -6.83865330383419, -6.623203350799344],
        #    'lon':[107.67049155274123, 107.65680155798631, 107.8216913262112, 107.63393542941085, 107.69114493759467, 107.52356300786431, 107.59553557341613],
        #    'sizeDot':[10, 100, 210, 10, 100, 210, 10 ],
        #    'colorDot':['red', 'green', 'yellow','red', 'green', 'yellow', 'red'],
        # }, dtype=str)

        con = sqlite3.connect('main.db')
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM kordinat'):
            # for i in range(0,len(data)):
            if row[4] is not None:
                colorDot = self.getColorDot(row[6])
                sizeDot = self.getSizeDot(row[7])
                satukan = ' '
                folium.Circle(location=[row[4], row[5]],
                      radius=sizeDot, 
                      fill=True, 
                      tooltip="Tanggal WIB = {0}<br>Tanggal WITA = {1}<br>Tanggal WIT = {2}<br><br> <b><i>Klik untuk selengkapnya ..<i></b> {3}".format(row[1],row[2],row[3],satukan),
                      popup=folium.Popup("<b>Tanggal WIB</b> = {0}<br><b>Tanggal WITA</b> = {1}<br><b>Tanggal WIT</b> = {2}<br><br><b>Lintang</b> = {3}<br><b>Bujur</b> = {4}<br><br><b>Kedalaman</b> = {5}<br><b>Magnitudo</b> = {6}<br><br><b>Sumber</b> = {7}<br><b>Keterangan</b> = {8}<br><br><b>Wil</b> = {9}<br><br><b>Dir</b> = {10}<br>".format(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]), max_width=800),
                      fill_color=colorDot,
                      color=colorDot,
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
        btnBrowse = QPushButton('Browse File..')
        btnBrowse.clicked.connect(self.openFileNameDialog)       
        btnBrowse.setStyleSheet("""
                QPushButton{
                    height:30px;background-color:#b3b3b3; border:0px; border-radius:3px; padding:8px
                }
                QPushButton:hover{
                    background-color: #d9d9d9
                }
            """)
        submitBtnBrowse = QPushButton('Import Sekarang..')
        submitBtnBrowse.clicked.connect(self.importData)

        submitBtnBrowse.setStyleSheet("""
                QPushButton{
                    background-color:#1a8cff;border:0px; border-radius:3px; padding:4px; font-size:19px; color:white
                }
                QPushButton:hover{
                    background-color:#80bfff
                }
            """)
        lrule = QLabel('Ketentuan File .CSV yang bisa digunakan')
        self.lbrowse = QLabel('Browse File (.csv)')
        self.lbrowse.setStyleSheet("background-color:#f2f2f2; padding-left:5px")

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
    
    def getSizeDot(self, magnitudo):
        #10, 160, 310 sizedot
        sizeDot = 10
        if (magnitudo < 3):
            sizeDot = 10

        if (magnitudo >= 3) and (magnitudo < 5):
            sizeDot = 160

        if (magnitudo >= 5):
            sizeDot = 340

        return sizeDot


    def getColorDot(self, kedalaman):
        colorSizeDot = 'red'
        if (kedalaman > 0) and (kedalaman <= 60):
            colorSizeDot = 'red'

        if (kedalaman >= 61) and (kedalaman <= 300):
            colorSizeDot = 'yellow'

        if (kedalaman > 300):
            colorSizeDot = 'green'

        return colorSizeDot

    def listRule(self):
        listWidget = QListWidget()
        QListWidgetItem("1. File Harus .CSV", listWidget)
        QListWidgetItem("2. Urutan Kolom HARUS berurutan -> Tanggal WIB, Tanggal WITA, Tanggal WIT, Lintang, Bujur, Kedalaman, Magnitude, Sumber, Keterangan, Wilayah, Dir..", listWidget)
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
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("Pastikan file CVS benar !, Yakin akan melakukan import data ?")
            msgBox.setWindowTitle("Import data !")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msgBox.buttonClicked.connect(msgButtonClick)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                num = 0;
                with open(self.pathFileCsv, newline='') as csvfile:
                    spamreader = csv.reader(csvfile)
                    for row in spamreader:
                        if num >= 1:
                            con = sqlite3.connect('main.db')
                            cur = con.cursor()
                            cur.execute("insert into kordinat (tgl_wib, tgl_wita, tgl_wit, lintang, bujur, kedalaman, magnitude, sumber, keterangna, wil, dir) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}') ".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
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
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setHorizontalHeaderLabels(["Tanggal WIB", "Tanggal WITA", "Tanggal WIT","Lintang", "Bujur", "Kedalaman","Magnitude", "Sumber", "Keterangan", "Wilayah", "Dir"])


        # self.tableWidget.setRowCount(4)
        tindex = 0
        for row in cur.execute('SELECT * FROM kordinat'):
            # deleteButton.clicked.connect(self.deleteClicked)
            # btn = QtWidgets.QPushButton("delete_this_row")
            # btn.clicked.connect(self.delRow)
            r4 = " {0}".format(row[4])
            r5 = " {0}".format(row[5])
            r6 = " {0}".format(row[6])
            r7 = " {0}".format(row[7])

            self.tableWidget.setItem(tindex,0, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tindex,1, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tindex,2, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tindex,3, QtWidgets.QTableWidgetItem(r4))
            self.tableWidget.setItem(tindex,4, QtWidgets.QTableWidgetItem(r5))
            self.tableWidget.setItem(tindex,5, QtWidgets.QTableWidgetItem(r6))
            self.tableWidget.setItem(tindex,6, QtWidgets.QTableWidgetItem(r7))
            self.tableWidget.setItem(tindex,7, QtWidgets.QTableWidgetItem(row[8]))
            self.tableWidget.setItem(tindex,8, QtWidgets.QTableWidgetItem(row[9]))
            self.tableWidget.setItem(tindex,9, QtWidgets.QTableWidgetItem(row[10]))
            self.tableWidget.setItem(tindex,10, QtWidgets.QTableWidgetItem(row[11]))
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