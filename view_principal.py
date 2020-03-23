# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 22:35:30 2020

@author: Computador
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import controller
import pyqt5_aux

qt_tela_inicial = "telas/principal.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    switch_tela_cadastrar_meta = QtCore.pyqtSignal()
    switch_tela_gerenciar_meta = QtCore.pyqtSignal(int)

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

        self.btn_cadastrar_meta.pressed.connect(self.abrir_tela_cadastrar_meta)
        #QUANDO DUPLOCLICAR EM UMA META DIARIA
        self.tb_fazer_hoje.cellDoubleClicked.connect(self.abrir_tela_gerenciar_meta)
        self.btn_sair.pressed.connect(self.sair)

        colunas_fazer_essa_semana = ['Codigo', 'Objetivo', 'Meta diaria', 'Feito hoje']
        pyqt5_aux.resize_colunas_table_widget(self.tb_fazer_hoje, colunas_fazer_essa_semana)

        colunas_fazer_essa_semana = ['Objetivo', 'Meta semanal', 'Feito essa semana', 'Total concluido', 'Meta final']
        pyqt5_aux.resize_colunas_table_widget(self.tb_fazer_essa_semana, colunas_fazer_essa_semana)
    
    def carregar_table_fazer_hoje(self):
        #[[texto meta, quant hoje, quant feita]]
        metas_fazer_hoje = controller.listar_fazer_hoje()

        pyqt5_aux.carregar_dados_table_widget(self.tb_fazer_hoje, metas_fazer_hoje)
    
    def carregar_table_fazer_essa_semana(self):
        #[[texto meta, quant hoje, quant feita]]
        metas_fazer_essa_semana = controller.listar_fazer_essa_semana()

        pyqt5_aux.carregar_dados_table_widget(self.tb_fazer_essa_semana, metas_fazer_essa_semana)

    def carregar_list_metas_status(self):
        self.list_metas.clear()
        metas_em_andamento = controller.listar_metas_por_status(self.combo_status.currentIndex())
        self.list_metas.addItems(metas_em_andamento)
    
    def abrir_tela_cadastrar_meta(self):
        self.switch_tela_cadastrar_meta.emit()
    
    def abrir_tela_gerenciar_meta(self):
        linha = self.tb_fazer_hoje.currentRow()
        id_meta = self.tb_fazer_hoje.item(linha, 0)
        self.switch_tela_gerenciar_meta.emit(int(id_meta.text()))
    
    def sair(self):
        self.close()