# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 19:33:29 2021

@author: https://github.com/anapaulazampier

"""

import pandas as pd
import seaborn as sns

#   obs: Código do município de 6 digitos de JF é 313670 e o código de 7 digítos é 3136702

#leitura das bases 
datapath1 = 'D:\\Usuarios\\Dell\\Documents\\jf em dados\\violencia_segmg\\Banco Crimes Violentos - Atualizado 2012 a 2017.csv'
datapath2 = 'D:\\Usuarios\\Dell\\Documents\\jf em dados\\violencia_segmg\\Banco Crimes Violentos - Atualizado Maro 2021.csv'

df1 = pd.read_csv(datapath1, header=0,sep=';',parse_dates=[[4,5]])
df2 = pd.read_csv(datapath2, header=0,sep=';',parse_dates=[[4,5]])

#filtro para juiz de fora 
jf1217 = df1[df1['Cod IBGE']==313670]
jf1821 = df2[df2['Cod IBGE']==313670]

#concatenação das bases e limpeza das informações
jftot = pd.concat([jf1217,jf1821])
jftot.columns = ['data','registros','natureza','mun','cod_mun','RISP','RISPN','RMBH']
jftot_clean = jftot.drop(columns=['mun','cod_mun','RISP','RISPN','RMBH'])



#gráfico de casos totais/anos e evolução de tipo de registro/ano
pivot = pd.pivot_table(jftot_clean,index='data',columns='natureza',values='registros',aggfunc='sum')
pivot2 = pd.pivot_table(jftot_clean,index='data',columns='natureza',values='registros',aggfunc='sum',margins=True)


#e vamos de heatmap
heat = jftot_clean.drop(columns='natureza')
heat = heat.groupby('data')['registros'].sum()
heat = heat.reset_index()
heat['year'] = pd.DatetimeIndex(heat['data']).year
heat['month'] = pd.DatetimeIndex(heat['data']).month
heatseaborn = pd.pivot_table(heat,values='registros',index='month',columns='year')
ax = sns.heatmap(heatseaborn, cmap='Reds')


#exports 
heatseaborn.to_csv('heat_seaborn.csv')               #export da tabela dinamica para heatmap formato seaborn 
heat.to_csv('heat.csv')                              #export para construção do heatmap formato flourish 
pivot.to_csv('flourish.csv')                         #export serie historia margins = false 
pivot2.to_csv('flourish2.csv')                       #export serie historica margins = true 
jftot.to_csv('crimes_violentos_jf_2012a2021.csv')    #bases da segurança concatenadas e filtradas para juiz de fora