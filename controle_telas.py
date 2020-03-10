import sys
from PyQt5 import QtCore, QtWidgets, uic

import view_principal

import view_cadastro_meta

class Controller:

    def __init__(self):
        pass

    def abre_tela_principal(self):
        self.janela_view_principal = view_principal.MainWindow()
        self.janela_view_principal.switch_tela_cadastro_meta.connect(self.abre_tela_cadastro_meta)
        self.janela_view_principal.show()
    
    def abre_tela_cadastro_meta(self):
        self.janela_tela_cadastro_meta = view_cadastro_meta.MainWindow()
        self.janela_tela_cadastro_meta.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.abre_tela_principal()
    sys.exit(app.exec_())

sys._excepthook = sys.excepthook 
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback) 
    sys.exit(1) 
sys.excepthook = exception_hook 

if __name__ == "__main__":
    main()
