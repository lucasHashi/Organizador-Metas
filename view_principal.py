# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 22:35:30 2020

@author: Computador
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import controller

qt_tela_inicial = "telas/principal.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    switch_tela_cadastro_meta = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #CARREGA METAS EM ANDAMENTO
        self.carregar_list_metas_status()

        #CARREGA O QUE FAZER HOJE
        self.carregar_table_fazer_hoje()

        #CARREGA O QUE FAZER ESSA SEMANA
        self.carregar_table_fazer_essa_semana()

        self.combo_status.currentIndexChanged.connect(self.carregar_list_metas_status)

        self.btn_cadastrar_meta.pressed.connect(self.abrir_tela_resumo_geral)
        self.btn_sair.pressed.connect(self.sair)

        header = self.tb_fazer_hoje.horizontalHeader() 
        self.tb_fazer_hoje.setHorizontalHeaderLabels(['Objetivo', 'Meta diaria', 'Feito hoje'])
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        header = self.tb_fazer_essa_semana.horizontalHeader() 
        self.tb_fazer_essa_semana.setHorizontalHeaderLabels(['Objetivo', 'Meta semanal', 'Feito essa semana', 'Total concluido', 'Meta final'])
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
    
    def carregar_table_fazer_hoje(self):
        #[[texto meta, quant hoje, quant feita]]
        metas_fazer_hoje = controller.listar_fazer_hoje()

        self.tb_fazer_hoje.setRowCount(0)
        for linha in range(len(metas_fazer_hoje)):
            self.tb_fazer_hoje.insertRow(linha)
            for coluna in range(len(metas_fazer_hoje[0])):
                self.tb_fazer_hoje.setItem(linha,coluna, QtWidgets.QTableWidgetItem(str(metas_fazer_hoje[linha][coluna])))
    
    def carregar_table_fazer_essa_semana(self):
        #[[texto meta, quant hoje, quant feita]]
        metas_fazer_essa_semana = controller.listar_fazer_essa_semana()

        self.tb_fazer_essa_semana.setRowCount(0)
        for linha in range(len(metas_fazer_essa_semana)):
            self.tb_fazer_essa_semana.insertRow(linha)
            for coluna in range(len(metas_fazer_essa_semana[0])):
                self.tb_fazer_essa_semana.setItem(linha,coluna, QtWidgets.QTableWidgetItem(str(metas_fazer_essa_semana[linha][coluna])))

    def carregar_list_metas_status(self):
        self.list_metas.clear()
        metas_em_andamento = controller.listar_metas(self.combo_status.currentIndex())
        self.list_metas.addItems(metas_em_andamento)
    
    def abrir_tela_resumo_geral(self):
        self.switch_tela_cadastro_meta.emit()
    
    def sair(self):
        self.close()