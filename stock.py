import pandas as pd
import numpy as np
import chart_studio.plotly as py
import cufflinks as cf
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
#####
# Plotly funcionar no Jupyter Notebook
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()
import investpy as inv
import matplotlib.pyplot as plt
import datetime as dt
###############################################################################

def data_show(data,feature,titulo):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data[feature],
                    mode='lines',
                ))
    fig.layout.update(title_text=titulo + stock_choice,
                 xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

data_inicio = '01/01/2020'
data_fim = dt.date.today().strftime('%d/%m/%Y')
    
#Criando uma side bar

st.sidebar.header('AÇÕES B3')

#Carregando ações

stock = np.array(inv.stocks.get_stocks_list(country='brazil'))
stock_choice = st.sidebar.selectbox('Escolha sua ação', stock)

start_date = st.sidebar.text_input('Data início', data_inicio)
end_date = st.sidebar.text_input('Data final', data_fim)

start = pd.to_datetime(start_date)
end = pd.to_datetime(end_date)

if start > end:
    st.write('Data de início não pode ser menor que a data final')


stock_historic = inv.get_stock_historical_data(stock_choice, country= 'brazil',from_date = start_date, to_date = end_date)

st.title(stock_choice)

desc = inv.get_stock_company_profile(stock_choice, country='brazil', language='english')['desc']
st.markdown(desc)

st.title('Gráfico')
st.markdown('A data de início é 01/01/2020. Para vizualizar períodos mais longos, selecione no menu a esquerda a data desejada. Períodos muitos longos podem causar lentidão no dash.')

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# include candlestick with rangeselector
fig.add_trace(go.Candlestick(x=stock_historic.index,
                open=stock_historic['Open'], high=stock_historic['High'],
                low=stock_historic['Low'], close=stock_historic['Close'],name='Fechamento'),
               secondary_y=True)

# include a go.Bar trace for volumes
fig.add_trace(go.Bar(x=stock_historic.index, y=stock_historic['Volume'],name='Volume'),
               secondary_y=False)

fig.layout.yaxis2.showgrid=False
fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    
)
st.plotly_chart(fig)

st.title('Informações Financeiras (R$) - Trimestral')

df_renda = inv.stocks.get_stock_financial_summary(stock_choice, 'brazil', summary_type='income_statement', period='quarterly')
df_renda_pt = df_renda.rename(columns={'Total Revenue': 'Receita Total','Gross Profit': 'Lucro Bruto','Operating Income': 'Lucro Operacional','Net Income': 'Lucro Líquido'})

r = df_renda_pt.reset_index().iloc[::-1]
data_certa = r['Date'].dt.strftime("%d %b, %Y")

fig = go.Figure(data=[
    go.Bar(name='Receita Total', x=data_certa, y=r['Receita Total'],marker_color='rgb(26, 118, 255)'),
    go.Bar(name='Lucro Líquido', x=data_certa, y=r['Lucro Líquido'],marker_color='rgb(55, 83, 109)')
])
# Change the bar mode
fig.update_layout(barmode='group',  xaxis_title="Trimestre",
    yaxis_title="R$ (Milhares)",title="Demostração Financeira do Exercício")
st.plotly_chart(fig)

df_renda2 = inv.stocks.get_stock_financial_summary(stock_choice, 'brazil', summary_type='balance_sheet', period='quarterly')
df_renda2_pt = df_renda2.rename(columns={'Total Assets': 'Ativos','Total Liabilities': 'Passivos','Total Equity': 'Patrimônio Líquido'})
r2 = df_renda2_pt.reset_index().iloc[::-1]
t2 = r2['Date'].dt.strftime("%d %b, %Y")

fig = go.Figure(data=[
    go.Bar(name='Ativos', x=t2, y=r2['Ativos'],marker_color='rgb(26, 118, 255)'),
    go.Bar(name='Passivos', x=t2, y=r2['Passivos'],marker_color='rgb(55, 83, 109)'),
    go.Bar(name='Patrimônio Líquido', x=t2, y=r2['Patrimônio Líquido'],marker_color='rgb(95, 83, 109)')
])
# Change the bar mode
fig.update_layout(barmode='group',  xaxis_title="Trimestre",
    yaxis_title="R$ (Milhares)", title="Balanço Patrimonial")
st.plotly_chart(fig)

df_renda3 = inv.get_stock_financial_summary(stock_choice, 'brazil', summary_type='cash_flow_statement', period='quarterly')
df_renda3_pt = df_renda3.rename(columns={'Cash From Operating Activities': 'Fluxo de Caixa Operacional','Cash From Investing Activities': 'Fluxo de Caixa - Investimentos','Cash From Financing Activities': 'Fluxo de Caixa - Atividades Financeiras','Net Change in Cash':'Variação Líquida do Fluxo de Caixa'})
r3 = df_renda3_pt.reset_index().iloc[::-1]
t3 = r3['Date'].dt.strftime("%d %b, %Y")

fig = go.Figure(data=[
    go.Bar(name='Operacional', x=t3, y=r3['Fluxo de Caixa Operacional'],marker_color='rgb(26, 118, 255)'),
    go.Bar(name='Investimentos', x=t3, y=r3['Fluxo de Caixa - Investimentos'],marker_color='rgb(55, 83, 109)'),
    go.Bar(name='Atividades Financeiras', x=t3, y=r3['Fluxo de Caixa - Atividades Financeiras']),
    go.Bar(name='Variação Líquida', x=t3, y=r3['Variação Líquida do Fluxo de Caixa'])
])
# Change the bar mode
fig.update_layout(barmode='group',  xaxis_title="Trimestre",
    yaxis_title="R$ (Milhares)", title="Fluxo de Caixa")
st.plotly_chart(fig)
