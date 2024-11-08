import streamlit as st
import requests
import pandas as pd

st.title('DADOS BRUTOS')

url = 'https://labdados.com/produtos'

response = requests.get(url)

# dados = pd.DataFrame.from_dict(response.json())

# Verificar o status da resposta
if response.status_code != 200:
    st.error(f"Erro ao acessar a API: {response.status_code}")
    st.stop()

# Verificar se a resposta é JSON
try:
    dados = pd.DataFrame.from_dict(response.json())
except ValueError:
    st.error("Erro ao decodificar o JSON. Verifique o formato da resposta.")
    st.write(response.text)  # Mostrar o conteúdo da resposta para debug
    st.stop()

dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

with st.expander("Colunas"):
    colunas = st.multiselect("Selecione as Colunas", list(dados.columns), list(dados.columns))
    
st.sidebar.title("Filtros")
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())
    
with st.sidebar.expander('Categoria do produto'):
    categoria = st.multiselect('Selecione as categorias', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())
    
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0,5000))
    
with st.sidebar.expander('Frete da venda'):
    frete = st.slider('Frete', 0,250, (0,250))
    
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))
    
with st.sidebar.expander('Vendedor'):
    vendedores = st.multiselect('Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())
    
with st.sidebar.expander('Local da compra'):
    local_compra = st.multiselect('Selecione o local da compra', dados['Local da compra'].unique(), dados['Local da compra'].unique())
    
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliação da compra',1,5, value = (1,5))
    
with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento',dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())
    
with st.sidebar.expander('Quantidade de parcelas'):
    qtd_parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1,24))
    
query = """
    Produto in @produtos and \
        @preco[0] <= Preço <= @preco[1] and \
            @data_compra[0] <= `Data da Compra` <= @data_compra[1]
"""
dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f"A Tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas.")