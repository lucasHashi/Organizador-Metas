# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 20:32:17 2020

@author: Computador
"""

from datetime import date
import json

#-----------CONFIG BASICAS-----------
def inicia_banco():
    json_banco = {'prox_cod': 0, 'metas': {}}
    
    with open('db/db_metas.json', 'w') as db_json_file:
        json.dump(json_banco, db_json_file)

#-----------INSERTS-----------
def insert_nova_meta(dict_meta, dt_inicio, periodo):
    with open('db/db_metas.json', 'r') as db_json_file:
        db_json = json.load(db_json_file)
    
    cod = db_json['prox_cod']
    db_json['prox_cod'] += 1
    
    dt_criacao = str(date.today())
    status = 0
    dt_limite_inicial = dict_meta['dt_limite']
    
    meta = {'dt_inicio': dt_inicio, 'dt_criacao': dt_criacao, 'status': status,
            'dt_limite_inicial': dt_limite_inicial, 'periodo': periodo,
            'dt_fechamento': '', 'meta': dict_meta}
    
    db_json['metas'][str(cod)] = meta
    
    with open('db/db_metas.json', 'w') as db_json_file:
        json.dump(db_json, db_json_file)

#-----------SELECTS-----------
def select_meta_por_codigo(cod):
    with open('db/db_metas.json', 'r') as db_json_file:
        db_json = json.load(db_json_file)
    
    meta = db_json['metas'][str(cod)]['meta']
    
    return meta

def select_metas_por_status(status):
    with open('db/db_metas.json', 'r') as db_json_file:
        db_json = json.load(db_json_file)
    
    prox_cod = db_json['prox_cod']

    metas_status = []
    for cod in range(0, prox_cod, 1):
        try:
            meta = db_json['metas'][str(cod)]
            if(meta['status'] == status):
                metas_status.append(meta['meta'])
        except:
            pass
    
    return metas_status

#-----------UPDATES-----------
def atualiza_dados_dia(cod, dados_atualizados_dia, data):
    with open('db/db_metas.json', 'r') as db_json_file:
        db_json = json.load(db_json_file)
    
    db_json['metas'][str(cod)]['meta']['datas'][data] = dados_atualizados_dia
    
    with open('db/db_metas.json', 'w') as db_json_file:
        json.dump(db_json, db_json_file)

def atualiza_progresso_meta(cod, quant):
    with open('db/db_metas.json', 'r') as db_json_file:
        db_json = json.load(db_json_file)
    
    db_json['metas'][str(cod)]['meta']['concluido'] += quant
    
    with open('db/db_metas.json', 'w') as db_json_file:
        json.dump(db_json, db_json_file)

#-----------DELETE-----------
def fecha_meta(cod, status):
    with open('db/db_metas.json', 'r') as db_json_file:
        db_json = json.load(db_json_file)
    
    dados_meta = db_json['metas'][str(cod)]
    
    dados_meta['status'] = status
    dados_meta['dt_fechamento'] = str(date.today())
    
    




















if __name__ == "__main__":
    inicia_banco()
    
    
    
    
    
    
    
    
    