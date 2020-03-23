import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import controller
from datetime import date, datetime, timezone

qt_tela_inicial = "telas/gerenciar_meta.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_tela_inicial)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    switch_tela_gerenciar_meta = QtCore.pyqtSignal()

    def __init__(self, id_meta):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.meta_atual = controller.select_meta_completa(id_meta)

        self.carregar_dados_meta(id_meta)
        
        data_hoje = str(date.today())
        data_hoje = QtCore.QDate.fromString(data_hoje, 'yyyy-MM-dd')
        self.date_dt_inicial.setDate(data_hoje)
        self.date_dt_final.setDate(data_hoje)

        self.btn_cadastrar.pressed.connect(self.cadastrar)
        self.btn_limpar.pressed.connect(self.limpar)
        self.btn_sair.pressed.connect(self.sair)
    
    def carregar_dados_meta(self, id_meta):
        dt_inicio, verbo, quantidade, unidade, dt_final, periodo, dias_semana = controller.listar_meta_para_editar(id_meta)

        self.date_dt_inicial.setDate(dt_inicio)

        self.txt_verbo.setText(verbo)
        self.double_quantidade.setValue(quantidade)
        self.txt_unidade.setText(unidade)

        self.date_dt_final.setDate(dt_final)

        self.txt_periodo.setText(periodo)

        if(0 in dias_semana):
            self.check_segunda.setCheckState(2)
        if(1 in dias_semana):
            self.check_terca.setCheckState(2)
        if(2 in dias_semana):
            self.check_quarta.setCheckState(2)
        if(3 in dias_semana):
            self.check_quinta.setCheckState(2)
        if(4 in dias_semana):
            self.check_sexta.setCheckState(2)
        if(5 in dias_semana):
            self.check_sabado.setCheckState(2)
        if(6 in dias_semana):
            self.check_domingo.setCheckState(2)
    
    def editar(self):
        dt_inicio = self.date_dt_inicial.date()
        dt_inicio = datetime.strptime('{}/{}/{}'.format(dt_inicio.day(), dt_inicio.month(), dt_inicio.year()), '%d/%m/%Y')
        
        verbo = self.txt_verbo.text()
        quantidade = self.double_quantidade.value()
        unidade = self.txt_unidade.text()
        dt_limite = self.date_dt_final.date()
        dt_limite = datetime.strptime('{}/{}/{}'.format(dt_limite.day(), dt_limite.month(), dt_limite.year()), '%d/%m/%Y')
        
        if(self.validar_entradas(dt_inicio, verbo, quantidade, unidade, dt_limite)):
            periodo = self.combo_periodo.currentText()
            if('semanal' in periodo):
                periodo = 'semana'
                controller.editar_meta_to_divisao(self.meta_atual, self.meta_atual['codigo'], dt_inicio, verbo, quantidade, unidade, dt_limite, periodo)
            else:
                periodo = 'dia'
                dias_da_semana = []
                if(self.check_segunda.isChecked()): dias_da_semana.append(0)
                if(self.check_terca.isChecked()): dias_da_semana.append(1)
                if(self.check_quarta.isChecked()): dias_da_semana.append(2)
                if(self.check_quinta.isChecked()): dias_da_semana.append(3)
                if(self.check_sexta.isChecked()): dias_da_semana.append(4)
                if(self.check_sabado.isChecked()): dias_da_semana.append(5)
                if(self.check_domingo.isChecked()): dias_da_semana.append(6)

                controller.editar_meta_to_divisao(self.meta_atual, self.meta_atual['codigo'], dt_inicio, verbo, quantidade, unidade, dt_limite, periodo, dias_da_semana)
        else:
            #POPUP AVISANDO QUE TEM ALGO DE ERRADO
            print('Todos os campos devem ser preenchidos')
            pass

    def validar_entradas(self, dt_inicio, verbo, quantidade, unidade, dt_limite):
        #VALIDAR SE AS DATAS SAO RAZOAVEIS
        dt_inicio = date.toordinal(dt_inicio)
        dt_limite = date.toordinal(dt_limite)
        if(dt_limite <= dt_inicio):
            return False

        if((not verbo) or (not unidade) or (quantidade <= 0)):
            return False
        
        #PEGAR O PERIODO
        periodo = self.combo_periodo.currentText()
        #SE O PERIODO FOR dia, CHECAR SE PELO MENOS UM DIA ESTA ESCOLHIDO
        if('diaria' in periodo):
            if(not (
                self.check_segunda.isChecked() or
                self.check_terca.isChecked() or
                self.check_quarta.isChecked() or
                self.check_quinta.isChecked() or
                self.check_sexta.isChecked() or
                self.check_sabado.isChecked() or
                self.check_domingo.isChecked()
                )):
                return False

        return True
    
    def sair(self):
        self.close()