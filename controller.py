# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 12:57:55 2020

@author: Computador
"""

from datetime import date, datetime, timezone
import model
import pprint
from PyQt5 import QtCore

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

#--------------CADASTRAR--------------
def meta_to_divisao(dt_inicio, verbo, quant, unid, dt_limite, periodo, dias_da_semana = [0]):
    if(periodo == 'dia'):
        meta_to_divisao_diaria(dt_inicio, verbo, quant, unid, dt_limite, dias_da_semana)
    elif(periodo == 'semana'):
        meta_to_divisao_semanal(dt_inicio, verbo, quant, unid, dt_limite)
    else:
        pass

def meta_to_divisao_diaria(dt_inicio, verbo, quant, unid, dt_limite, dias_da_semana):
    dt_inicio = dt_inicio.toordinal()
    dt_limite = dt_limite.toordinal()
    
    dict_dias_trabalho = {'restantes': 0,
                          'concluido': 0,
                          'dt_limite': str(date.fromordinal(dt_limite)),
                          'dias_da_semana': dias_da_semana,
                          'meta': quant,
                          'unidade': unid,
                          'verbo': verbo,
                          'divisao': 0,
                          'atualizado': str(date.today()),
                          'datas': {}
                          }
    for i_ordi in range(dt_inicio, dt_limite, 1):
        data_atual = date.fromordinal(i_ordi)
        dict_dias_trabalho['datas'][str(data_atual)] = {'feito': 0, 'meta_atingida': 0, 'dia_ativo': 0}
        if(data_atual.weekday() in dias_da_semana):
            dict_dias_trabalho['datas'][str(data_atual)]['dia_ativo'] = 1
            dict_dias_trabalho['restantes'] += 1
    
    dias_restantes = dict_dias_trabalho['restantes']
    dict_dias_trabalho['divisao'] = round(quant/dias_restantes, 2)
    
    pprint.pprint(dict_dias_trabalho)
    
    model.insert_nova_meta(dict_dias_trabalho, str(date.fromordinal(dt_inicio)), 'dia')

def meta_to_divisao_semanal(dt_inicio, verbo, quant, unid, dt_limite):
    dt_inicio = dt_inicio.toordinal()
    dt_limite = dt_limite.toordinal()
    
    dict_dias_trabalho = {'restantes': 0,
                          'concluido': 0,
                          'dt_limite': str(date.fromordinal(dt_limite)),
                          'meta': quant,
                          'unidade': unid,
                          'verbo': verbo,
                          'divisao': 0,
                          'atualizado': str(date.today()),
                          'datas': {}
                          }
    
    for i_ordi in range(dt_inicio, dt_limite, 1):
        data_atual = date.fromordinal(i_ordi)
        if(data_atual.weekday() == 0):#SE ESTE DIA FOR UMA SEGUNDA-FEIRA
            dict_dias_trabalho['datas'][str(data_atual)] = {'feito': 0, 'meta_atingida': 0}
            dict_dias_trabalho['restantes'] += 1
    
    semanas_restantes = dict_dias_trabalho['restantes']
    dict_dias_trabalho['divisao'] = round(quant/semanas_restantes, 2)
    
    pprint.pprint(dict_dias_trabalho)
    
    model.insert_nova_meta(dict_dias_trabalho, str(date.fromordinal(dt_inicio)), 'semana')

#--------------LISTAR--------------
#VARIAS METAS
def listar_metas_por_status(status):
    #SELECT DAS METAS COM status == status
    metas_status = model.select_metas_por_status(status)

    metas_textos = []
    for meta in metas_status:
        data_final = datetime.strptime(meta['dt_limite'], '%Y-%m-%d')
        
        texto = '{} {} {} ate {}'.format(meta['verbo'], meta['meta'], meta['unidade'], data_final.strftime('%Y-%m-%d'))
        metas_textos.append(texto)

    return metas_textos

def listar_fazer_hoje():
    metas_andamento = model.select_metas_por_status(0)

    #[[texto meta, quant hoje, quant feita]]
    fazer_hoje = []
    for meta in metas_andamento:
        codigo = meta['codigo']
        texto = '{} {} {}'.format(meta['verbo'], meta['meta'], meta['unidade'])
        quant_hoje = meta['divisao']
        quant_feita_hoje = meta['datas'][str(date.today())]['feito']
        fazer_hoje.append([codigo, texto, quant_hoje, quant_feita_hoje])
    
    return fazer_hoje

def listar_fazer_essa_semana():
    metas_andamento = model.select_metas_por_status(0)

    dias_dessa_semana = listar_dias_dessa_semana(str(date.today()))

    #[[texto meta, quant semana, quant feita, meta final]]
    fazer_essa_semana = []
    for meta in metas_andamento:
        texto = '{} {} {}'.format(meta['verbo'], meta['meta'], meta['unidade'])
        quant_essa_semana = meta['divisao'] * len(meta['dias_da_semana'])

        quant_feita_essa_semana = 0
        for dia in dias_dessa_semana:
            if(meta['datas'][dia]['dia_ativo']):
                quant_feita_essa_semana += meta['datas'][dia]['feito']

        fazer_essa_semana.append([texto, quant_essa_semana, quant_feita_essa_semana, meta['concluido'], meta['meta']])
    
    return fazer_essa_semana

def select_meta_completa(id_meta):
    
    return model.select_meta_por_codigo(id_meta)


#--------------EDITAR--------------
def editar_meta_to_divisao(meta_base, id_meta, dt_inicio, verbo, quant, unid, dt_limite, periodo, dias_da_semana = [0]):
    if(periodo == 'dia'):
        editar_meta_to_divisao_diaria(meta_base, id_meta, dt_inicio, verbo, quant, unid, dt_limite, dias_da_semana)
    elif(periodo == 'semana'):
        editar_meta_to_divisao_semanal(meta_base, id_meta, dt_inicio, verbo, quant, unid, dt_limite)
    else:
        pass

def editar_meta_to_divisao_diaria(meta_base, id_meta, dt_inicio, verbo, quant, unid, dt_limite, dias_da_semana):
    dt_inicio = dt_inicio.toordinal()
    dt_limite = dt_limite.toordinal()

    concluido = meta_base['meta']['concluido']
    
    dict_dias_trabalho = {'restantes': 0,
                          'concluido': concluido,
                          'dt_limite': str(date.fromordinal(dt_limite)),
                          'dias_da_semana': dias_da_semana,
                          'meta': quant,
                          'unidade': unid,
                          'verbo': verbo,
                          'divisao': 0,
                          'atualizado': str(date.today()),
                          'datas': {}
                          }
    for i_ordi in range(dt_inicio, dt_limite, 1):
        data_atual = date.fromordinal(i_ordi)
        dict_dias_trabalho['datas'][str(data_atual)] = {'feito': 0, 'meta_atingida': 0, 'dia_ativo': 0}
        if(data_atual.weekday() in dias_da_semana):
            dict_dias_trabalho['datas'][str(data_atual)]['dia_ativo'] = 1
            dict_dias_trabalho['restantes'] += 1
    
    dias_restantes = dict_dias_trabalho['restantes']
    dict_dias_trabalho['divisao'] = round(quant/dias_restantes, 2)
    
    pprint.pprint(dict_dias_trabalho)
    
    model.editar_meta(dict_dias_trabalho, str(date.fromordinal(dt_inicio)), 'dia', id_meta)

def editar_meta_to_divisao_semanal(meta_base, id_meta, dt_inicio, verbo, quant, unid, dt_limite):
    dt_inicio = dt_inicio.toordinal()
    dt_limite = dt_limite.toordinal()
    
    dict_dias_trabalho = {'restantes': 0,
                          'concluido': 0,
                          'dt_limite': str(date.fromordinal(dt_limite)),
                          'meta': quant,
                          'unidade': unid,
                          'verbo': verbo,
                          'divisao': 0,
                          'atualizado': str(date.today()),
                          'datas': {}
                          }
    
    for i_ordi in range(dt_inicio, dt_limite, 1):
        data_atual = date.fromordinal(i_ordi)
        if(data_atual.weekday() == 0):#SE ESTE DIA FOR UMA SEGUNDA-FEIRA
            dict_dias_trabalho['datas'][str(data_atual)] = {'feito': 0, 'meta_atingida': 0}
            dict_dias_trabalho['restantes'] += 1
    
    semanas_restantes = dict_dias_trabalho['restantes']
    dict_dias_trabalho['divisao'] = round(quant/semanas_restantes, 2)
    
    pprint.pprint(dict_dias_trabalho)
    
    model.editar_meta(dict_dias_trabalho, str(date.fromordinal(dt_inicio)), 'semana', id_meta)

#--------------UNICA META--------------
def listar_meta_para_editar(id_meta):
    #SELECT DA META DO CODIGO id_meta
    meta_completa = model.select_meta_por_codigo(id_meta)

    dt_inicio = meta_completa['dt_inicio']
    verbo = meta_completa['meta']['verbo']
    quantidade = meta_completa['meta']['meta']
    unidade = meta_completa['meta']['unidade']
    dt_final = meta_completa['meta']['dt_limite']
    periodo = meta_completa['periodo']
    dias_semana = meta_completa['meta']['dias_da_semana']

    dt_inicio = QtCore.QDate.fromString(dt_inicio, 'yyyy-MM-dd')
    dt_final = QtCore.QDate.fromString(dt_final, 'yyyy-MM-dd')
    
    if(periodo == 'dia'):
        periodo = 'diaria'
    elif(periodo == 'semana'):
        periodo = 'semanal'

    return dt_inicio, verbo, quantidade, unidade, dt_final, periodo, dias_semana
    

#--------------OUTROS--------------
def listar_dias_dessa_semana(data):
    #DIAS DESSA SEMANA: ['ano-mes-dia', 'ano-mes-dia', ...]
    dia_base = datetime.strptime(data, '%Y-%m-%d')
    dia_base_ord = date.toordinal(dia_base)
    dia_semana = dia_base.weekday()

    dias_semana = []
    for dia_ord in range(dia_base_ord - dia_semana, dia_base_ord + 7 - dia_semana, 1):
        dia_atual = date.fromordinal(dia_ord)
        dias_semana.append(str(dia_atual))
    
    return dias_semana

#--------------ATUALIZAR--------------
def cadastra_progresso(cod, quant, data):
    meta = model.select_meta_por_codigo(cod)
    
    dados_do_dia = meta['datas'][data]
    
    dados_do_dia['feito'] += quant
    
    meta_diaria = meta['divisao']
    if(quant >= meta_diaria):
        dados_do_dia['meta_atingida'] = 1
    
    model.atualiza_dados_dia(cod, dados_do_dia, data)
    
    model.atualiza_progresso_meta(cod, quant)



#--------------TESTES--------------
#model.inicia_banco()

#Juntar 10000 reais até 01/01/2023, me preocupando 1 dia por semana
#meta_to_divisao('2020-03-09', 'juntar', 10000, 'reais', '2023-01-01', 'semana')

#Traduzir 15000 palavras até 01/04/2020, me preocupando 5 dias por semana
#meta_to_divisao('2020-03-01','traduzir', 15000, 'palavras', '2020-04-01', 'dia', [0,1,2,3,4])

#cadastra_progresso(1, 1000, '2020-03-15')
#cadastra_progresso(0, 70, '2020-03-09')


























