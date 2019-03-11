#from PyQt5 import uic
from PyQt4 import uic

# Load the .ui file
DialogUi , DialogType = uic.loadUiType('C:/Users/da2/Documents/scripts_python_qgis/5_items.ui')

# A class for logic defined in the user interface
class MyDialog (DialogType , DialogUi):
    def __init__ (self):
        super(MyDialog, self).__init__()
        self.setupUi(self)
        
        self.cb_1.addItem("Python")
        
        self.bt_1.clicked.connect(self.buttonClicked)
        self.cb_1.currentIndexChanged.connect(self.comboboxChanged)
        
    def buttonClicked(self):
        text = self.cb_1.currentText()
        self.le_1.setText(text)
        
    def comboboxChanged(self):
        text = self.cb_1.currentText()
        iface.messageBar().pushMessage(text)
        
dialog = MyDialog()
dialog.show()

# dialog.exec_ ()