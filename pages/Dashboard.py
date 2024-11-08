import streamlit as st
import requests
import pandas as pd
import plotly.express as px


def  format_number(value, prefix=""):
    for unidade in ["", "mil"]:
        if value < 1000:
            return f"{prefix} {value:.2f} {unidade}"
        value /= 1000
    
    return f"{prefix} {value:.2f} milhões"

st.title("DASHBOARD DE VENDAS :shopping_trolley:")

url = "https://labdados.com/produtos"
regioes = ["Brasil", "Centro-Oeste", "Nordeste", "Norte", "Sudeste", "Sul"]

st.sidebar.title("Filtros")
regiao = st.sidebar.selectbox("Região", regioes)

if regiao == "Brasil":
    regiao = ""

todos_anos = st.sidebar.checkbox("Dados de todo o período", value=True)
if todos_anos:
    ano = ""
else:
    ano = st.sidebar.slider("Ano", 2020, 2023)

query_string = {
    "regiao": regiao.lower(),
    "ano": ano
}

response = requests.get(url, params=query_string)
dados = pd.DataFrame.from_dict(response.json())
dados["Data da Compra"] = pd.to_datetime(dados["Data da Compra"], format="%d/%m/%Y")

filtro_vendedores = st.sidebar.multiselect("Vendedores", dados["Vendedor"].unique())
if filtro_vendedores:
    dados = dados[dados["Vendedor"].isin(filtro_vendedores)]

## Tabelas

# ====================================== TABS - RECEITA ======================================

# Receita - Estado
receita_estados = dados.groupby("Local da compra")[["Preço"]].sum()
receita_estados = dados.drop_duplicates(subset="Local da compra")[["Local da compra", "lat", "lon"]].merge(
    receita_estados, 
    left_on="Local da compra", 
    right_index=True
    ).sort_values('Preço', ascending=False)

# Receita - Datas
receita_mensal = dados.set_index("Data da Compra").groupby(pd.Grouper(freq="M"))["Preço"].sum().reset_index()
receita_mensal["Ano"] = receita_mensal["Data da Compra"].dt.year
receita_mensal["Mes"] = receita_mensal["Data da Compra"].dt.month_name()

# Receita - Categorias
receita_categorias = dados.groupby("Categoria do Produto")["Preço"].sum().sort_values(ascending=False)

# ====================================== TABS - VENDAS ======================================

# Vendas- Estado
venda_estados = dados.groupby("Local da compra")[["Preço"]].count()
venda_estados = dados.drop_duplicates(subset="Local da compra")[["Local da compra", "lat", "lon"]].merge(
    venda_estados, 
    left_on="Local da compra", 
    right_index=True
    ).sort_values('Preço', ascending = False)

# Vendas - Datas
venda_mensal = dados.set_index("Data da Compra").groupby(pd.Grouper(freq="M"))["Preço"].count().reset_index()
venda_mensal["Ano"] = venda_mensal["Data da Compra"].dt.year
venda_mensal["Mes"] = venda_mensal["Data da Compra"].dt.month_name()

# Vendas - Categorias
venda_categorias = dados.groupby("Categoria do Produto")["Preço"].count().sort_values(ascending=False)

# ====================================== TABS - VENDEDORES ======================================

vendedores = pd.DataFrame(dados.groupby("Vendedor")["Preço"].agg(["sum", "count"]))


## Gráficos

# ====================================== ABA 1 - RECEITA ======================================

# Mapa
fig_mapa_receita = px.scatter_geo(
    receita_estados,
    lat="lat",
    lon="lon",
    scope="south america",
    size="Preço",
    template="seaborn",
    hover_name="Local da compra",
    hover_data={"lat": False, "lon": False},
    title="Mapa de Receita por Estado",
    )
fig_mapa_receita.update_layout(yaxis_title="Receita")

# Linhas
fig_receita_mensal = px.line(
    receita_mensal,
    x="Mes",
    y="Preço",
    markers=True,
    range_y=(0, receita_mensal.max()),
    color="Ano",
    line_dash="Ano",
    title="Receita Mensal"
)
fig_receita_mensal.update_layout(yaxis_title="Receita")

# Barra 1
fig_receita_estados = px.bar(
    receita_estados.head(),
    x="Local da compra",
    y="Preço",
    text_auto=True,
    title="Top Estados (Receita)",
)
fig_receita_estados.update_layout(yaxis_title="Receita")

# Barra 2
fig_receita_categorias = px.bar(
    receita_categorias,
    text_auto=True,
    title= "Receita por categoria"
)
fig_receita_categorias.update_layout(yaxis_title="Receita")


# ====================================== ABA 2 - VENDAS ======================================

# Mapa
fig_mapa_vendas = px.scatter_geo(
    venda_estados,
    lat="lat",
    lon="lon",
    scope="south america",
    size="Preço",
    template="seaborn",
    hover_name="Local da compra",
    hover_data={"lat": False, "lon": False},
    title="Vendas por estado",
    )
fig_mapa_vendas.update_layout(yaxis_title="Vendas por estado")

# Linhas
fig_venda_mensal = px.line(
    venda_mensal,
    x="Mes",
    y="Preço",
    markers=True,
    range_y=(0, receita_mensal.max()),
    color="Ano",
    line_dash="Ano",
    title="Quantidade de vendas mensal"
)
fig_mapa_vendas.update_layout(yaxis_title="Quantidade de vendas")

# Barra 1
fig_venda_estados = px.bar(
    venda_estados.head(),
    x="Local da compra",
    y="Preço",
    text_auto=True,
    title="Top Estados (Vendas)",
)
fig_venda_estados.update_layout(yaxis_title="Quantidade de vendas")

# Barra 2
fig_venda_categorias = px.bar(
    venda_categorias,
    text_auto=True,
    title= "Vendas por categoria"
)
fig_venda_categorias.update_layout(showlegend=False, yaxis_title="Vendas")



## Visualização Streamlit
aba1, aba2, aba3 = st.tabs(["Receita", "Quantidade de Vendas", "Vendedores"])

# Receita
with aba1:
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Receita", format_number(dados["Preço"].sum(), "R$"))
        st.plotly_chart(fig_mapa_receita, use_container_width=True)
        st.plotly_chart(fig_receita_estados, use_container_width=True)

    with col2:
        st.metric("Quantidade de Vendas", format_number(dados.shape[0]))
        st.plotly_chart(fig_receita_mensal, use_container_width=True)
        st.plotly_chart(fig_receita_categorias, use_container_width=True)

# Vendas
with aba2:
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Receita", format_number(dados["Preço"].sum(), "R$"))
        st.plotly_chart(fig_mapa_vendas, use_container_width=True)
        st.plotly_chart(fig_venda_estados, use_container_width=True)


    with col2:
        st.metric("Quantidade de Vendas", format_number(dados.shape[0]))
        st.plotly_chart(fig_venda_mensal, use_container_width=True)
        st.plotly_chart(fig_venda_categorias, use_container_width=True)

# Vendedores
with aba3:
    qtd_vendedores = st.number_input("Quantidade de Vendedores", 2, 10, 5)
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Receita", format_number(dados["Preço"].sum(), "R$"))
        
        fig_receita_vendedores = px.bar(
            vendedores[["sum"]].sort_values("sum", ascending=False).head(qtd_vendedores),
            x="sum",
            y=vendedores[["sum"]].sort_values("sum", ascending=False).head(qtd_vendedores).index,
            text_auto=True,
            title=f"Top {qtd_vendedores} Vendedores (Receita)"
        )
        st.plotly_chart(fig_receita_vendedores)


    with col2:
        st.metric("Quantidade de Vendas", format_number(dados.shape[0]))
        
        fig_vendas_vendedores = px.bar(
            vendedores[["count"]].sort_values("count", ascending=False).head(qtd_vendedores),
            x="count",
            y=vendedores[["count"]].sort_values("count", ascending=False).head(qtd_vendedores).index,
            text_auto=True,
            title=f"Top {qtd_vendedores} Vendedores (Qtd. Vendas)"
        )
        
        st.plotly_chart(fig_vendas_vendedores)
 
    

