import streamlit as st
import requests
import pandas as pd
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def succes_mesage():
    # A barra de progresso aparece depois de clicar no botão de download
    progress_text = "Download in progress. Please, wait..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    
    sucesso = st.success("Download feito com sucesso!", icon="✅")
    time.sleep(5)
    sucesso.empty()
    
# st.set_page_config(page_title="Aplicativo de Vendas", layout="wide", page_icon=":shopping_cart:")
st.set_page_config(page_title="DADOS BRUTOS", layout="wide")
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

query = '''
Produto in @produtos and \
    `Categoria do Produto` in @categoria and \
        @preco[0] <= Preço <= @preco[1] and \
            @frete[0] <= Frete <= @frete[1] and \
                @data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
                    Vendedor in @vendedores and \
                        `Local da compra` in @local_compra and \
                            @avaliacao[0]<= `Avaliação da compra` <= @avaliacao[1] and \
                                `Tipo de pagamento` in @tipo_pagamento and \
                                    @qtd_parcelas[0] <= `Quantidade de parcelas` <= @qtd_parcelas[1]
'''

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f"A Tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas.")

st.markdown("Escreva um nome para o arquivo")

col1, col2 = st.columns(2)
with col1:
    nome_arquivo = st.text_input("", label_visibility='collapsed', value="dados")
    nome_arquivo += ".csv"
    
with col2:
    st.download_button("Download", data=converte_csv(dados_filtrados), file_name=nome_arquivo, mime="text/csv", on_click=succes_mesage)
