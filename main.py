#! /usr/bin/env python3
import sys
from BankRecord import BankRecord
from BelfiusParser import BelfiusParser
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *

import faulthandler
faulthandler.enable()

from mainWindow import Ui_MainWindow

class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return BankRecord.getMaxIdx()

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()].getIdxData(index.column()))

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Vertical:
            return QVariant()
        if role != Qt.DisplayRole:
            return QVariant()
        return QVariant(BankRecord.getIdxHeaderData(section))

class FilterHeader(QHeaderView):
    filterActivated = QtCore.pyqtSignal()

    def __init__(self, count, parent):
        super(QHeaderView, self).__init__(QtCore.Qt.Horizontal, parent)
        self._editors = []
        self._padding = 4
        self.setStretchLastSection(True)
        self.setSectionResizeMode(QHeaderView.Interactive)
        self.setDefaultAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.setSortIndicatorShown(False)
        self.sectionResized.connect(self.adjustPositions)
        parent.horizontalScrollBar().valueChanged.connect(
            self.adjustPositions)
        self.setFilterBoxes(count)

    def setFilterBoxes(self, count):
        while self._editors:
            editor = self._editors.pop()
            editor.deleteLater()
        for index in range(count):
            editor = QLineEdit(self.parent())
            editor.setPlaceholderText('Filter')
            editor.textChanged.connect(self.filterActivated.emit)
            self._editors.append(editor)
        self.adjustPositions()

    def sizeHint(self):
        size = super(QHeaderView, self).sizeHint()
        if self._editors:
            height = self._editors[0].sizeHint().height()
            #size.setHeight(size.height() + height + self._padding)
            size.setHeight(55)
        return size

    def updateGeometries(self):
        if self._editors:
            height = self._editors[0].sizeHint().height()
            self.setViewportMargins(0, 0, 0, height + self._padding)
        else:
            self.setViewportMargins(0, 0, 0, 0)
        super(QHeaderView, self).updateGeometries()
        self.adjustPositions()

    def adjustPositions(self):
        for index, editor in enumerate(self._editors):
            height = editor.sizeHint().height()
            editor.move(
                self.sectionPosition(index) - self.offset() + 2,
                height + (self._padding // 2))
            editor.resize(self.sectionSize(index), height)

    def filterText(self, index):
        if 0 <= index < len(self._editors):
            return self._editors[index].text()
        return ''

    def setFilterText(self, index, text):
        if 0 <= index < len(self._editors):
            self._editors[index].setText(text)

    def clearFilters(self):
        for editor in self._editors:
            editor.clear()

class RecordFilter(QSortFilterProxyModel):
    def __init__(self, parent):
        super(QSortFilterProxyModel,self).__init__(parent)
        self.filterHeader = None

    def setFilterHeader(self, filterHeader):
        self.filterHeader = filterHeader

    def filterAcceptsRow(self, source_row, source_parent):
        sourceModel = self.sourceModel()
        if not self.filterHeader:
            return False
        for i in range(BankRecord.getMaxIdx()):
            idx = sourceModel.index(source_row, i, source_parent)
            dataString = sourceModel.data(idx, Qt.DisplayRole).value().lower()
            filterText = self.filterHeader.filterText(i).lower()
            #print("'%s' '%s'"%(dataString, filterText))
            if len(filterText) > 0 and not dataString.find(filterText) >= 0:
                #print("FALSE")
                return False
        #print("TRUE")
        return True

class App(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        super(Ui_MainWindow, self).__init__()
        self.title = 'Bank Record Analyzer'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 600
        self.currentRecords = []

        self.initUI()

    def initUI(self):
        #print("init  UI\n")
        self.setupUi(self)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.tableModel = MyTableModel(self.currentRecords, self)
        self.proxy = RecordFilter(self)
        self.proxy.setSourceModel(self.tableModel)
        self.tableView.setModel(self.proxy)
        self.customHeader = FilterHeader(BankRecord.getMaxIdx(), self.tableView)
        self.tableView.setHorizontalHeader(self.customHeader)
        self.tableView.setColumnWidth(0, 200)
        self.tableView.setColumnWidth(1, 100)
        self.tableView.setColumnWidth(2, 500)
        self.tableView.setColumnWidth(3, 100)
        self.proxy.setFilterHeader(self.customHeader)
        self.tableView.verticalHeader().setDefaultSectionSize(100)

        self.connectSignals()
        self.showMaximized()

    def connectSignals(self):
        #print("connecting signals\n")
        self.actionOpen.triggered.connect(self.openBelfiusFile)
        self.actionQuit.triggered.connect(self.close)
        self.customHeader.filterActivated.connect(self.handleFilterActivated)

    def handleFilterActivated(self):
        self.tableModel.layoutChanged.emit()

    def openBelfiusFile(self):
        parser = BelfiusParser()
        self.openFileWithParser(parser)

    def openFileWithParser(self, parser):
        dlg = QFileDialog()
        fileFilter = parser.getFileTypeToOpen()
        fileNames, _ = QFileDialog.getOpenFileNames(self, "Open Images", '',
                fileFilter)
        if fileNames:
            #print(fileNames)
            parserRecords = parser.parseRecords(fileNames)
            #print "parserRecords: %s"%(parserRecords)
            #print "self.currentRecords: %s"%(self.currentRecords)
            for curRec in parserRecords:
                if curRec not in self.currentRecords:
                    self.currentRecords += [curRec]
            #print "after self.currentRecords: %s"%(self.currentRecords)
            self.currentRecords.sort(reverse=True)
            #print(self.currentRecords)
            self.tableView.resizeRowsToContents()
            self.tableModel.layoutChanged.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
