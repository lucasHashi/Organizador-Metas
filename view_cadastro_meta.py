import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import controller

qt_tela_inicial = "telas/cadastro_meta.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    switch_tela_cadastro_meta = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn_cadastrar.pressed.connect(self.cadastrar)
        self.btn_limpar.pressed.connect(self.limpar)
        self.btn_sair.pressed.connect(self.sair)
    
    def cadastrar(self):
        #meta_to_divisao(dt_inicio, verbo, quant, unid, dt_limite, periodo, dias_da_semana = [0])
        dt_inicio = self.date_dt_inicial.date()
        verbo = self.txt_verbo.text()
        quantidade = self.double_quantidade.value()
        unidade = self.txt_unidade.text()
        dt_limite = self.date_dt_final.date()
        
        if(self.validar_entradas(dt_inicio, verbo, quantidade, unidade, dt_limite)):
            #PEGAR TEXTO DO PERIODO
            periodo = 'sim'
            if('semanal' in periodo):
                periodo = 'semana'
                controller.meta_to_divisao(dt_inicio, verbo, quantidade, unidade, dt_limite, periodo)
            else:
                periodo = 'dia'
                dias_da_semana = []
                if('#SE A CHECK seg ESTIVER CLICADA'): dias_da_semana.append(0)
                if('#SE A CHECK ter ESTIVER CLICADA'): dias_da_semana.append(1)
                if('#SE A CHECK qua ESTIVER CLICADA'): dias_da_semana.append(2)
                if('#SE A CHECK qui ESTIVER CLICADA'): dias_da_semana.append(3)
                if('#SE A CHECK sex ESTIVER CLICADA'): dias_da_semana.append(4)
                if('#SE A CHECK sab ESTIVER CLICADA'): dias_da_semana.append(5)
                if('#SE A CHECK dom ESTIVER CLICADA'): dias_da_semana.append(6)

                controller.meta_to_divisao(dt_inicio, verbo, quantidade, unidade, dt_limite, periodo, dias_da_semana)
        else:
            #POPUP AVISANDO QUE TEM ALGO DE ERRADO
            print('Todos os campos devem ser preenchidos')
            pass

    def validar_entradas(self, dt_inicio, verbo, quantidade, unidade, dt_limite):
        datas,textos,dias_semana = 0,0,0
        
        #VALIDAR SE AS DATAS SAO RAZOAVEIS
        datas = 1

        if(verbo and unidade and quantidade > 0):
            textos = 1
        
        #PEGAR O PERIODO
        #SE O PERIODO FOR dia, CHECAR SE PELO MENOS UM DIA ESTA ESCOLHIDO
        dias_semana = 1

        return datas*textos*dias_semana

    def limpar(self):
        #SETAR DATA INICIAL PARA HOJE
        self.txt_verbo.clear()
        self.double_quantidade.clear()
        self.txt_unidade.clear()
        #SETAR DATA FINAL PARA HOJE
        #SETAR COMBO PERIODO PARA INDICE 0

        #FOCO PARA DATA INICIAL
    
    def sair(self):
        self.close()