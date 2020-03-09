# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 12:57:55 2020

@author: Computador
"""

from datetime import date, datetime, timezone
import model_teste
import pprint

'''
ENTRADAS
- Data inicio
- Verbo/Nome
- Quantidade
- Unidade
- Data limite
- Dias da semana de trabalho

SAIDAS
- Dict:
    {restantes: int, concluido: float, dt_limite: date,
    dias_da_semana: list, meta: float, unidade: str,
    verbo: str, divisao: float, atualizado: data,
    datas:
        {'ano-mes-dia':
            {feito: float, meta_atingida: bool, 'dia_ativo': bool},
            {feito: float, meta_atingida: bool, 'dia_ativo': bool},
            ...
        }objetivo
    }
'''

def meta_to_divisao(dt_inicio, verbo, quant, unid, data_limite, periodo, dias_da_semana = [0]):
    if(periodo == 'dia'):
        meta_to_divisao_diaria(dt_inicio, verbo, quant, unid, data_limite, dias_da_semana)
    elif(periodo == 'semana'):
        meta_to_divisao_semanal(dt_inicio, verbo, quant, unid, data_limite)
    else:
        pass

def meta_to_divisao_diaria(dt_inicio, verbo, quant, unid, data_limite, dias_da_semana):
    data_limite = datetime.strptime(data_limite, '%Y-%m-%d')
    dt_inicio = datetime.strptime(dt_inicio, '%Y-%m-%d')
    
    dt_inicio = dt_inicio.toordinal()
    data_limite = data_limite.toordinal()
    
    dict_dias_trabalho = {'restantes': 0,
                          'concluido': 0,
                          'dt_limite': str(date.fromordinal(data_limite)),
                          'dias_da_semana': dias_da_semana,
                          'meta': quant,
                          'unidade': unid,
                          'verbo': verbo,
                          'divisao': 0,
                          'atualizado': str(date.today()),
                          'datas': {}
                          }
    for i_ordi in range(dt_inicio, data_limite, 1):
        data_atual = date.fromordinal(i_ordi)
        dict_dias_trabalho['datas'][str(data_atual)] = {'feito': 0, 'meta_atingida': 0, 'dia_ativo': 0}
        if(data_atual.weekday() in dias_da_semana):
            dict_dias_trabalho['datas'][str(data_atual)]['dia_ativo'] = 1
            dict_dias_trabalho['restantes'] += 1
    
    dias_restantes = dict_dias_trabalho['restantes']
    dict_dias_trabalho['divisao'] = round(quant/dias_restantes, 2)
    
    pprint.pprint(dict_dias_trabalho)
    
    model_teste.insert_nova_meta(dict_dias_trabalho, str(date.fromordinal(dt_inicio)), 'dia')

def meta_to_divisao_semanal(dt_inicio, verbo, quant, unid, data_limite):
    data_limite = datetime.strptime(data_limite, '%Y-%m-%d')
    dt_inicio = datetime.strptime(dt_inicio, '%Y-%m-%d')
    
    dt_inicio = dt_inicio.toordinal()
    data_limite = data_limite.toordinal()
    
    dict_dias_trabalho = {'restantes': 0,
                          'concluido': 0,
                          'dt_limite': str(date.fromordinal(data_limite)),
                          'meta': quant,
                          'unidade': unid,
                          'verbo': verbo,
                          'divisao': 0,
                          'atualizado': str(date.today()),
                          'datas': {}
                          }
    
    for i_ordi in range(dt_inicio, data_limite, 1):
        data_atual = date.fromordinal(i_ordi)
        if(data_atual.weekday() == 0):#SE ESTE DIA FOR UMA SEGUNDA-FEIRA
            dict_dias_trabalho['datas'][str(data_atual)] = {'feito': 0, 'meta_atingida': 0}
            dict_dias_trabalho['restantes'] += 1
    
    semanas_restantes = dict_dias_trabalho['restantes']
    dict_dias_trabalho['divisao'] = round(quant/semanas_restantes, 2)
    
    pprint.pprint(dict_dias_trabalho)
    
    model_teste.insert_nova_meta(dict_dias_trabalho, str(date.fromordinal(dt_inicio)), 'semana')

def cadastra_progresso(cod, quant, data):
    meta = model_teste.select_meta_por_codigo(cod)
    
    dados_do_dia = meta['datas'][data]
    
    dados_do_dia['feito'] += quant
    
    meta_diaria = meta['divisao']
    if(quant >= meta_diaria):
        dados_do_dia['meta_atingida'] = 1
    
    model_teste.atualiza_dados_dia(cod, dados_do_dia, data)
    
    model_teste.atualiza_progresso_meta(cod, quant)



#--------------TESTES--------------
model_teste.inicia_banco()

#Juntar 10000 reais até 01/01/2023, me preocupando 1 dia por semana
meta_to_divisao('2020-03-09', 'juntar', 10000, 'reais', '2023-01-01', 'semana')

#Traduzir 15000 palavras até 01/04/2020, me preocupando 5 dias por semana
meta_to_divisao('2020-03-01','traduzir', 15000, 'palavras', '2020-04-01', 'dia', [0,1,2,3,4])

cadastra_progresso(1, 1000, '2020-03-15')
cadastra_progresso(0, 70, '2020-03-09')


























