import streamlit as st

# Configuração da página (deve ser o primeiro comando)
st.set_page_config(page_title="Aplicativo de Vendas", layout="wide", page_icon=":shopping_cart:")

# Título da aplicação
st.title("Aplicativo de Vendas :bar_chart:")

# Seção de introdução
st.markdown("""
Bem-vindo ao **Aplicativo de Vendas**! A plataforma para você explorar e visualizar interativamente os dados de vendas da sua empresa. 
Com esta ferramenta, você pode tomar decisões mais informadas com base nas análises de desempenho, segmentação de mercado e muito mais.
""")

# Inserir imagem (opcional)
st.image("https://www.example.com/imagem-do-app.png", width=600)  # Substitua pela URL da imagem do seu app

# Seção de navegação
st.markdown("## Navegação")
st.markdown("""
Escolha uma das seções abaixo para explorar os dados de vendas:

- **Dashboard de Vendas**
  - Visualize gráficos e métricas de vendas.
- **Dados Brutos**
  - Acesse e filtre os dados brutos das vendas.
- **Sobre**
  - Informações sobre o aplicativo e a tecnologia por trás dele.
""")

# Seção de explicação
st.markdown("""
## Funcionalidades Principais
O **Aplicativo de Vendas** permite que você:
- Analise o desempenho de vendas por **região**, **categoria** de produto, **vendedor**, entre outros.
- Explore os **dados brutos** de vendas com filtros interativos.
- Visualize tendências de **crescimento** e **comportamento do cliente**.

""")

# Sobre o aplicativo
st.markdown("## Sobre o Aplicativo")
st.markdown("""
Este aplicativo foi desenvolvido para fornecer **insights** valiosos sobre suas vendas. Com ele, você poderá:
- Monitorar e analisar dados em tempo real.
- Visualizar gráficos interativos de vendas.
- Tomar decisões mais ágeis e eficazes com base nos dados.
""")
st.markdown("Desenvolvido por **Kaue Santana**.")

# Recursos Tecnológicos
st.markdown("### Tecnologias Utilizadas:")
st.markdown("""
- **Python** (Streamlit, Pandas, Plotly)
- **API** para integração e coleta de dados de vendas
- **Gráficos interativos** para visualização de dados
- **Mapas de calor** para análise de regiões
""")

# Dicas para o usuário
st.markdown("### Dicas de Uso:")
st.markdown("""
1. Ao acessar o **Dashboard**, explore os gráficos e veja as métricas chave.
2. Use o painel de **Filtros** nos **Dados Brutos** para segmentar as vendas por diferentes parâmetros.
3. Caso queira voltar para a página inicial, clique no ícone no topo da barra lateral.
""")
