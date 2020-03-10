# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 22:35:30 2020

@author: Computador
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

qt_tela_inicial = "telas/principal.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    switch_tela_cadastro_meta = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn_cadastrar_meta.pressed.connect(self.abrir_tela_resumo_geral)
        self.btn_sair.pressed.connect(self.sair)
    
    def abrir_tela_resumo_geral(self):
        self.switch_tela_cadastro_meta.emit()
    
    def sair(self):
        self.close()