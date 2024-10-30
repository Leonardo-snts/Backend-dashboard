import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Carregar os dados CSV gerados anteriormente
@st.cache_data
def load_data():
    return pd.read_csv("data/dados_dash.csv")

data = load_data()

# Título da aplicação
st.title("Análise de Distribuidora de Produtos para E-commerce")

# Mostrar os dados na aplicação
st.subheader("Visualização dos Dados")
st.write(data)

# Gráfico 1: Contagem de produtos vendidos por tipo de produto
st.subheader("Gráfico 1: Contagem de Produtos por Tipo de Produto")
fig1 = px.histogram(data, x="tipo do produto", title="Contagem de Produtos por Tipo de Produto")
st.plotly_chart(fig1)\

# Gráfico 2: Distribuição de vendas por loja
st.subheader("Gráfico 2: Vendas por Loja")
fig2 = px.histogram(data, x="loja que comprou", title="Distribuição de Vendas por Loja")
st.plotly_chart(fig2)

# Gráfico 3: Valor total de venda por tipo de produto
st.subheader("Gráfico 3: Valor Total de Venda por Tipo de Produto")
fig3 = px.bar(data.groupby('tipo do produto').sum().reset_index(), x="tipo do produto", y="valor de venda", title="Valor Total de Venda por Tipo de Produto")
st.plotly_chart(fig3)

# Gráfico 4: Valor de compra vs valor de venda (scatter plot)
st.subheader("Gráfico 4: Comparação de Valor de Compra vs Valor de Venda")
fig4 = px.scatter(data, x="valor de compra", y="valor de venda", color="tipo do produto", title="Valor de Compra vs Valor de Venda")
st.plotly_chart(fig4)

# Gráfico 5: Quantidade comprada por loja
st.subheader("Gráfico 5: Quantidade Comprada por Loja")
fig5 = px.bar(data.groupby('loja que comprou').sum().reset_index(), x="loja que comprou", y="quantidade comprada", title="Quantidade Comprada por Loja")
st.plotly_chart(fig5)

# Gráfico 6: Tipos de envio usados nas vendas
st.subheader("Gráfico 6: Frequência dos Tipos de Envio")
fig6 = px.pie(data, names="tipo de envio", title="Tipos de Envio")
st.plotly_chart(fig6)

# Gráfico 7: Status de entrega por loja
st.subheader("Gráfico 7: Status de Entrega por Loja")
fig7 = px.histogram(data, x="loja que comprou", color="status de entrega", title="Status de Entrega por Loja")
st.plotly_chart(fig7)

# Gráfico 8: Quantidade comprada por moeda usada
st.subheader("Gráfico 8: Quantidade Comprada por Moeda")
fig8 = px.bar(data.groupby('moeda usada').sum().reset_index(), x="moeda usada", y="quantidade comprada", title="Quantidade Comprada por Moeda Usada")
st.plotly_chart(fig8)

# Gráfico 9: Valor de venda total por moeda usada
st.subheader("Gráfico 9: Valor Total de Venda por Moeda Usada")
fig9 = px.bar(data.groupby('moeda usada').sum().reset_index(), x="moeda usada", y="valor de venda", title="Valor Total de Venda por Moeda")
st.plotly_chart(fig9)
 
# Gráfico 10: Comparação de preços entre lojas e distribuidora
st.subheader("Gráfico 10: Comparação de Preços entre Lojas e Distribuidora")
fig10 = go.Figure()
fig10.add_trace(go.Box(y=data["preço distribuidora"], name="Distribuidora", boxpoints="all"))
fig10.add_trace(go.Box(y=data["preço loja 1"], name="Loja 1", boxpoints="all"))
fig10.add_trace(go.Box(y=data["preço loja 2"], name="Loja 2", boxpoints="all"))
fig10.update_layout(title="Distribuição de Preços: Distribuidora vs Lojas")
st.plotly_chart(fig10)

# Gráfico 11: Valor de venda por cidade
st.subheader("Gráfico 11: Valor de Venda por Cidade de Envio")
fig11 = px.bar(data.groupby('cidade do envio').sum().reset_index(), x="cidade do envio", y="valor de venda", title="Valor de Venda por Cidade")
st.plotly_chart(fig11)

# Gráfico 12: Média de valor de venda por tipo de produto (Apenas colunas numéricas)
st.subheader("Gráfico 12: Média de Valor de Venda por Tipo de Produto")
numeric_columns = ['valor de venda']  # Especificando as colunas numéricas
fig12 = px.bar(data.groupby('tipo do produto')[numeric_columns].mean().reset_index(), x="tipo do produto", y="valor de venda", title="Média de Valor de Venda por Tipo de Produto")
st.plotly_chart(fig12)

# Gráfico 13: Média de valor de compra por tipo de produto (Apenas colunas numéricas)
st.subheader("Gráfico 13: Média de Valor de Compra por Tipo de Produto")
numeric_columns = ['valor de compra']  # Especificando as colunas numéricas
fig13 = px.bar(data.groupby('tipo do produto')[numeric_columns].mean().reset_index(), x="tipo do produto", y="valor de compra", title="Média de Valor de Compra por Tipo de Produto")
st.plotly_chart(fig13)

# Gráfico 14: Quantidade de produtos comprados por mês
st.subheader("Gráfico 14: Quantidade Comprada por Mês")
data['data da venda'] = pd.to_datetime(data['data da venda'])
data['mes'] = data['data da venda'].dt.month
fig14 = px.histogram(data, x='mes', y='quantidade comprada', title="Quantidade de Produtos Comprados por Mês")
st.plotly_chart(fig14)

# Gráfico 15: Canal de venda utilizado
st.subheader("Gráfico 15: Distribuição dos Canais de Venda")
fig15 = px.pie(data, names="canal de venda", title="Distribuição dos Canais de Venda")
st.plotly_chart(fig15)

# Gráfico 16: Quantidade comprada por tipo de envio
st.subheader("Gráfico 16: Quantidade Comprada por Tipo de Envio")
fig16 = px.bar(data.groupby('tipo de envio').sum(numeric_only=True).reset_index(), x="tipo de envio", y="quantidade comprada", title="Quantidade Comprada por Tipo de Envio")
st.plotly_chart(fig16)

# Gráfico 17: Valor total por status de entrega
st.subheader("Gráfico 17: Valor Total por Status de Entrega")
fig17 = px.bar(data.groupby('status de entrega').sum(numeric_only=True).reset_index(), x="status de entrega", y="valor de venda", title="Valor Total por Status de Entrega")
st.plotly_chart(fig17)

# Gráfico 18: Quantidade de vendas por status de entrega
st.subheader("Gráfico 18: Quantidade de Vendas por Status de Entrega")
fig18 = px.histogram(data, x="status de entrega", title="Quantidade de Vendas por Status de Entrega")
st.plotly_chart(fig18)

# Gráfico 19: Comparação de valor de venda por canal de venda
st.subheader("Gráfico 19: Comparação de Valor de Venda por Canal de Venda")
fig19 = px.bar(data.groupby('canal de venda').sum(numeric_only=True).reset_index(), x="canal de venda", y="valor de venda", title="Comparação de Valor de Venda por Canal de Venda")
st.plotly_chart(fig19)

# Gráfico 20: Valor de venda por estado de envio
st.subheader("Gráfico 20: Valor de Venda por Estado de Envio")
fig20 = px.bar(data.groupby('estado do envio').sum(numeric_only=True).reset_index(), x="estado do envio", y="valor de venda", title="Valor de Venda por Estado de Envio")
st.plotly_chart(fig20)