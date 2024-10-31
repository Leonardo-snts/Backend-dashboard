from flask import jsonify, Blueprint
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go
from api.funcao import create_heatmap, data
from flask_cors import cross_origin

api = Blueprint('api', __name__)

@api.route('/grafico1', methods=['GET'])
def grafico1():
    fig = px.histogram(data, x="tipo do produto", title="1. Contagem de Produtos por Tipo de Produto")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico2', methods=['GET'])
def grafico2():
    fig = px.histogram(data, x="loja que comprou", title="2. Distribuição de Vendas por Loja")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico3', methods=['GET'])
def grafico3():
    fig =  px.bar(data.groupby('tipo do produto').sum().reset_index(), x="tipo do produto", y="valor de venda", title="3. Valor Total de Venda por Tipo de Produto")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico4', methods=['GET'])
def grafico4():
    fig =  px.scatter(data, x="valor de compra", y="valor de venda", color="tipo do produto", title="4. Valor de Compra vs Valor de Venda")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico5', methods=['GET'])
def grafico5():
    fig =  px.bar(data.groupby('loja que comprou').sum().reset_index(), x="loja que comprou", y="quantidade comprada", title="5. Quantidade Comprada por Loja")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico6', methods=['GET'])
def grafico6():
    fig =  px.pie(data, names="tipo de envio", title="6. Tipos de Envio")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico7', methods=['GET'])
def grafico7():
    fig =  px.histogram(data, x="loja que comprou", color="status de entrega", title="7. Status de Entrega por Loja")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico8', methods=['GET'])
def grafico8():
    fig =  px.bar(data.groupby('moeda usada').sum().reset_index(), x="moeda usada", y="quantidade comprada", title="8. Quantidade Comprada por Moeda Usada")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico9', methods=['GET'])
def grafico9():
    fig =  px.bar(data.groupby('moeda usada').sum().reset_index(), x="moeda usada", y="valor de venda", title="9. Valor Total de Venda por Moeda")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico10', methods=['GET'])
def grafico10():
    fig =  go.Figure()
    fig.add_trace(go.Box(y=data["preço distribuidora"], name="Distribuidora", boxpoints="all"))
    fig.add_trace(go.Box(y=data["preço loja 1"], name="Loja 1", boxpoints="all"))
    fig.add_trace(go.Box(y=data["preço loja 2"], name="Loja 2", boxpoints="all"))
    fig.update_layout(title="10. Distribuição de Preços: Distribuidora vs Lojas")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico11', methods=['GET'])
def grafico11():
    data_filtered = data.select_dtypes(exclude=['datetime64[ns]'])
    fig = px.bar(data.groupby('cidade do envio').sum().reset_index(), x="cidade do envio", y="valor de venda", title="11. Valor de Venda por Cidade")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico12', methods=['GET'])
def grafico12():
    numeric_columns = ['valor de venda']  # Especificando as colunas numéricas
    fig = px.bar(data.groupby('tipo do produto')[numeric_columns].mean().reset_index(), x="tipo do produto", y="valor de venda", title="12. Média de Valor de Venda por Tipo de Produto")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico13', methods=['GET'])
def grafico13():
    numeric_columns = ['valor de compra']  # Especificando as colunas numéricas
    fig = px.bar(data.groupby('tipo do produto')[numeric_columns].mean().reset_index(), x="tipo do produto", y="valor de compra", title="13. Média de Valor de Compra por Tipo de Produto")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico14', methods=['GET'])
def grafico14():
    data['data da venda'] = pd.to_datetime(data['data da venda'])
    data['mes'] = data['data da venda'].dt.month
    fig = px.histogram(data, x='mes', y='quantidade comprada', title="14. Quantidade de Produtos Comprados por Mês")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico15', methods=['GET'])
def grafico15():
    fig = px.pie(data, names="canal de venda", title="15. Distribuição dos Canais de Venda")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico16', methods=['GET'])
def grafico16():
    fig = px.bar(data.groupby('tipo de envio').sum(numeric_only=True).reset_index(), x="tipo de envio", y="quantidade comprada", title="16. Quantidade Comprada por Tipo de Envio")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico17', methods=['GET'])
def grafico17():
    fig = px.bar(data.groupby('status de entrega').sum(numeric_only=True).reset_index(), x="status de entrega", y="valor de venda", title="17. Valor Total por Status de Entrega")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico18', methods=['GET'])
def grafico18():
    fig = px.histogram(data, x="status de entrega", title="18. Quantidade de Vendas por Status de Entrega")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico19', methods=['GET'])
def grafico19():
    fig = px.bar(data.groupby('canal de venda').sum(numeric_only=True).reset_index(), x="canal de venda", y="valor de venda", title="19. Comparação de Valor de Venda por Canal de Venda")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico20', methods=['GET'])
def grafico20():
    fig = px.bar(data.groupby('estado do envio').sum(numeric_only=True).reset_index(), x="estado do envio", y="valor de venda", title="20. Valor de Venda por Estado de Envio")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@api.route('/grafico21', methods=['GET'])
@cross_origin()
def grafico21():
    # Agrupar os dados por diferentes níveis
    data_city = data.groupby(['cidade do envio', 'latitude', 'longitude']).sum().reset_index()
    data_state = data.groupby(['estado do envio', 'pais do envio']).sum().reset_index()
    data_country = data.groupby(['pais do envio']).sum().reset_index()

    # Criar o layout inicial
    fig = create_heatmap(data_city, 'cidade')

    # Adicionar um dropdown para selecionar cidade, estado ou país
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        args=[{"data": [go.Scattergeo(
                            lat=data_city['latitude'],
                            lon=data_city['longitude'],
                            marker=dict(size=data_city['quantidade comprada'], color=data_city['quantidade comprada'], colorscale="Viridis"),
                            hovertext=data_city['cidade do envio'],
                        )]}],
                        label="Cidade",
                        method="update"
                    ),
                    dict(
                        args=[{"data": [go.Scattergeo(
                            locations=data_state['estado do envio'],
                            locationmode='country names',  # Ajustado para funcionar com estados de qualquer país
                            marker=dict(size=data_state['quantidade comprada'], color=data_state['quantidade comprada'], colorscale="Viridis"),
                            hovertext=data_state['estado do envio'],
                        )]}],
                        label="Estado",
                        method="update"
                    ),
                    dict(
                        args=[{"data": [go.Scattergeo(
                            locations=data_country['pais do envio'],
                            locationmode='country names',
                            marker=dict(size=data_country['quantidade comprada'], color=data_country['quantidade comprada'], colorscale="Viridis"),
                            hovertext=data_country['pais do envio'],
                        )]}],
                        label="País",
                        method="update"
                    ),
                ],
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
            ),
        ]
    )

    # Converter o gráfico para JSON
    graph_json = pio.to_json(fig)
    
    # Retornar o JSON como resposta
    return jsonify(graph_json)

# área de clientes
@api.route('/clientes', methods=['GET'])
def clientes_graficos():
    # Filtra apenas colunas numéricas para o agrupamento
    numeric_data = data.select_dtypes(include=['number'])
    grouped_data = data.groupby('loja que comprou')[numeric_data.columns].sum().reset_index()
    
    # Gráfico 2: Distribuição de Vendas por Loja
    fig2 = px.histogram(data, x="loja que comprou", title="2. Distribuição de Vendas por Loja")
    graph_json2 = pio.to_json(fig2)

    # Gráfico 5: Quantidade Comprada por Loja
    fig5 = px.bar(grouped_data, x="loja que comprou", y="quantidade comprada", title="5. Quantidade Comprada por Loja")
    graph_json5 = pio.to_json(fig5)

    # Gráfico 6: Tipos de Envio
    fig6 = px.pie(data, names="tipo de envio", title="6. Tipos de Envio")
    graph_json6 = pio.to_json(fig6)

    # Gráfico 7: Status de Entrega por Loja
    fig7 = px.histogram(data, x="loja que comprou", color="status de entrega", title="7. Status de Entrega por Loja")
    graph_json7 = pio.to_json(fig7)

    # Gráfico 10: Distribuição de Preços - Distribuidora vs Lojas
    fig10 = go.Figure()
    fig10.add_trace(go.Box(y=data["preço distribuidora"], name="Distribuidora", boxpoints="all"))
    fig10.add_trace(go.Box(y=data["preço loja 1"], name="Loja 1", boxpoints="all"))
    fig10.add_trace(go.Box(y=data["preço loja 2"], name="Loja 2", boxpoints="all"))
    fig10.update_layout(title="10. Distribuição de Preços: Distribuidora vs Lojas")
    graph_json10 = pio.to_json(fig10)

    # Retornando todos os gráficos em um único JSON
    return jsonify({
        "grafico2": graph_json2,
        "grafico5": graph_json5,
        "grafico6": graph_json6,
        "grafico7": graph_json7,
        "grafico10": graph_json10
    })

# área de vendas
@api.route('/vendas', methods=['GET'])
def vendas_grafico():
    data_filtered = data.select_dtypes(exclude=['datetime64[ns]'])
    # Gráfico 3
    fig3 = px.bar(data.groupby('tipo do produto').sum(numeric_only=True).reset_index(), x="tipo do produto", y="valor de venda", title="3. Valor Total de Venda por Tipo de Produto")
    graph_json3 = pio.to_json(fig3)

    # Gráfico 4
    fig4 = px.scatter(data, x="valor de compra", y="valor de venda", color="tipo do produto", title="4. Valor de Compra vs Valor de Venda")
    graph_json4 = pio.to_json(fig4)

    # Gráfico 8
    fig8 = px.bar(data.groupby('moeda usada').sum(numeric_only=True).reset_index(), x="moeda usada", y="quantidade comprada", title="8. Quantidade Comprada por Moeda Usada")
    graph_json8 = pio.to_json(fig8)
    
    # Gráfico 9 
    fig9 = px.bar(data.groupby('moeda usada').sum(numeric_only=True).reset_index(), x="moeda usada", y="valor de venda", title="9. Valor Total de Venda por Moeda")
    graph_json9 = pio.to_json(fig9)

    # Gráfioc 12
    numeric_columns = ['valor de venda']  # Especificando as colunas numéricas
    fig12 = px.bar(data.groupby('tipo do produto')[numeric_columns].mean().reset_index(), x="tipo do produto", y="valor de venda", title="12. Média de Valor de Venda por Tipo de Produto")
    graph_json12 = pio.to_json(fig12)

    # Gráfico 13
    numeric_columns = ['valor de compra']  # Especificando as colunas numéricas
    fig13 = px.bar(data.groupby('tipo do produto')[numeric_columns].mean().reset_index(), x="tipo do produto", y="valor de compra", title="13. Média de Valor de Compra por Tipo de Produto")
    graph_json13 = pio.to_json(fig13)

    return jsonify({
        "grafico3": graph_json3,
        "grafico4": graph_json4,
        "grafico8": graph_json8,
        "grafico9": graph_json9,
        "grafico12": graph_json12,
        "grafico13": graph_json13
    })

# área de Produtos
@api.route('/produtos', methods=['GET'])
def produtos_grafico():
    data_filtered = data.select_dtypes(exclude=['datetime64[ns]'])
    # Gráfico 1 
    fig1 = px.histogram(data, x="tipo do produto", title="1. Contagem de Produtos por Tipo de Produto")
    graph_json1 = pio.to_json(fig1)

    # Gráfico 14 
    data['data da venda'] = pd.to_datetime(data['data da venda'])
    data['mes'] = data['data da venda'].dt.month
    fig14 = px.histogram(data, x='mes', y='quantidade comprada', title="14. Quantidade de Produtos Comprados por Mês")
    graph_json14 = pio.to_json(fig14)

    # Gráfico 15
    fig15 = px.pie(data, names="canal de venda", title="15. Distribuição dos Canais de Venda")
    graph_json15 = pio.to_json(fig15)

    # Gráfico 16
    fig16 = px.bar(data.groupby('tipo de envio').sum(numeric_only=True).reset_index(), x="tipo de envio", y="quantidade comprada", title="16. Quantidade Comprada por Tipo de Envio")
    graph_json16 = pio.to_json(fig16)

    # Gráfico 17
    fig17 = px.bar(data.groupby('status de entrega').sum(numeric_only=True).reset_index(), x="status de entrega", y="valor de venda", title="17. Valor Total por Status de Entrega")
    graph_json17 = pio.to_json(fig17)

    # Gráfico 18
    fig18 = px.histogram(data, x="status de entrega", title="18. Quantidade de Vendas por Status de Entrega")
    graph_json18 = pio.to_json(fig18)

    # Gráfico 19
    fig19 = px.bar(data.groupby('canal de venda').sum(numeric_only=True).reset_index(), x="canal de venda", y="valor de venda", title="19. Comparação de Valor de Venda por Canal de Venda")
    graph_json19 = pio.to_json(fig19)

    return jsonify({
        "grafico1": graph_json1,
        "grafico14": graph_json14,
        "grafico15": graph_json15,
        "grafico16": graph_json16,
        "grafico17": graph_json17,
        "grafico18": graph_json18,
        "grafico19": graph_json19
    })

# área de mapa
@api.route('/mapa', methods=['GET'])
def mapa_grafico():
    # Gráfico 11
    data_filtered = data.select_dtypes(exclude=['datetime64[ns]'])
    fig11 = px.bar(data.groupby('cidade do envio').sum(numeric_only=True).reset_index(), x="cidade do envio", y="valor de venda", title="11. Valor de Venda por Cidade")
    graph_json11 = pio.to_json(fig11)
    
    # Gráfico 20
    fig20 = px.bar(data.groupby('estado do envio').sum(numeric_only=True).reset_index(), x="estado do envio", y="valor de venda", title="20. Valor de Venda por Estado de Envio")
    graph_json20 = pio.to_json(fig20)

    # Gráfico21
    # Agrupar os dados por diferentes níveis
    data_city = data.groupby(['cidade do envio', 'latitude', 'longitude']).sum(numeric_only=True).reset_index()
    data_state = data.groupby(['estado do envio', 'pais do envio']).sum(numeric_only=True).reset_index()
    data_country = data.groupby(['pais do envio']).sum(numeric_only=True).reset_index()

    # Criar o layout inicial
    fig21 = create_heatmap(data_city, 'cidade')

    # Adicionar um dropdown para selecionar cidade, estado ou país
    fig21.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        args=[{"data": [go.Scattergeo(
                            lat=data_city['latitude'],
                            lon=data_city['longitude'],
                            marker=dict(size=data_city['quantidade comprada'], color=data_city['quantidade comprada'], colorscale="Viridis"),
                            hovertext=data_city['cidade do envio'],
                        )]}],
                        label="Cidade",
                        method="update"
                    ),
                    dict(
                        args=[{"data": [go.Scattergeo(
                            locations=data_state['estado do envio'],
                            locationmode='country names',  # Ajustado para funcionar com estados de qualquer país
                            marker=dict(size=data_state['quantidade comprada'], color=data_state['quantidade comprada'], colorscale="Viridis"),
                            hovertext=data_state['estado do envio'],
                        )]}],
                        label="Estado",
                        method="update"
                    ),
                    dict(
                        args=[{"data": [go.Scattergeo(
                            locations=data_country['pais do envio'],
                            locationmode='country names',
                            marker=dict(size=data_country['quantidade comprada'], color=data_country['quantidade comprada'], colorscale="Viridis"),
                            hovertext=data_country['pais do envio'],
                        )]}],
                        label="País",
                        method="update"
                    ),
                ],
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
            ),
        ]
    )

    # Converter o gráfico para JSON
    graph_json21 = pio.to_json(fig21)

    return jsonify({
        "grafico11": graph_json11,
        "grafico20": graph_json20,
        "grafico21": graph_json21,
    })