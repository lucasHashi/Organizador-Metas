import sys
from PyQt5 import QtCore, QtWidgets, uic
import pyqt5_aux

def carregar_dados_table_widget(tabela, lista):
    tabela.setRowCount(0)
    for linha in range(len(lista)):
        tabela.insertRow(linha)
        for coluna in range(len(lista[0])):
            tabela.setItem(linha,coluna, QtWidgets.QTableWidgetItem(str(lista[linha][coluna])))

def resize_colunas_table_widget(tabela, titulos_colunas, resize_primeira = True):
    header = tabela.horizontalHeader() 
    tabela.setHorizontalHeaderLabels(titulos_colunas)

    inicio = 0
    if(not resize_primeira):
        inicio += 1

    for coluna in range(inicio, len(titulos_colunas), 1):
        header.setSectionResizeMode(coluna, QtWidgets.QHeaderView.ResizeToContents)