from flask import Flask, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Função para carregar dados
def load_data():
    return pd.read_csv("data/dados_dash.csv")

data = load_data()

# Endpoint para o gráfico 1
@app.route('/grafico1', methods=['GET'])
def grafico1():
    fig = px.histogram(data, x="tipo do produto", title="1. Contagem de Produtos por Tipo de Produto")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

# Adicionar mais endpoints para outros gráficos conforme necessário
# Exemplo para gráfico 2:
@app.route('/grafico2', methods=['GET'])
def grafico2():
    fig = px.histogram(data, x="loja que comprou", title="2. Distribuição de Vendas por Loja")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico3', methods=['GET'])
def grafico3():
    fig =  px.bar(data.groupby('tipo do produto').sum().reset_index(), x="tipo do produto", y="valor de venda", title="3. Valor Total de Venda por Tipo de Produto")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico4', methods=['GET'])
def grafico4():
    fig =  px.scatter(data, x="valor de compra", y="valor de venda", color="tipo do produto", title="4. Valor de Compra vs Valor de Venda")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico5', methods=['GET'])
def grafico5():
    fig =  px.bar(data.groupby('loja que comprou').sum().reset_index(), x="loja que comprou", y="quantidade comprada", title="5. Quantidade Comprada por Loja")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico6', methods=['GET'])
def grafico6():
    fig =  px.pie(data, names="tipo de envio", title="6. Tipos de Envio")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico7', methods=['GET'])
def grafico7():
    fig =  px.histogram(data, x="loja que comprou", color="status de entrega", title="7. Status de Entrega por Loja")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico8', methods=['GET'])
def grafico8():
    fig =  px.bar(data.groupby('moeda usada').sum().reset_index(), x="moeda usada", y="quantidade comprada", title="8. Quantidade Comprada por Moeda Usada")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico9', methods=['GET'])
def grafico9():
    fig =  px.bar(data.groupby('moeda usada').sum().reset_index(), x="moeda usada", y="valor de venda", title="9. Valor Total de Venda por Moeda")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico10', methods=['GET'])
def grafico10():
    fig =  go.Figure()
    fig.add_trace(go.Box(y=data["preço distribuidora"], name="Distribuidora", boxpoints="all"))
    fig.add_trace(go.Box(y=data["preço loja 1"], name="Loja 1", boxpoints="all"))
    fig.add_trace(go.Box(y=data["preço loja 2"], name="Loja 2", boxpoints="all"))
    fig.update_layout(title="10. Distribuição de Preços: Distribuidora vs Lojas")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico11', methods=['GET'])
def grafico11():
    fig = px.bar(data.groupby('cidade do envio').sum().reset_index(), x="cidade do envio", y="valor de venda", title="11. Valor de Venda por Cidade")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico12', methods=['GET'])
def grafico12():
    numeric_columns = ['valor de venda']  # Especificando as colunas numéricas
    fig = px.bar(data.groupby('tipo do produto')[numeric_columns].mean().reset_index(), x="tipo do produto", y="valor de venda", title="12. Média de Valor de Venda por Tipo de Produto")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico13', methods=['GET'])
def grafico13():
    numeric_columns = ['valor de compra']  # Especificando as colunas numéricas
    fig = px.bar(data.groupby('tipo do produto')[numeric_columns].mean().reset_index(), x="tipo do produto", y="valor de compra", title="13. Média de Valor de Compra por Tipo de Produto")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico14', methods=['GET'])
def grafico14():
    data['data da venda'] = pd.to_datetime(data['data da venda'])
    data['mes'] = data['data da venda'].dt.month
    fig = px.histogram(data, x='mes', y='quantidade comprada', title="14. Quantidade de Produtos Comprados por Mês")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico15', methods=['GET'])
def grafico15():
    fig = px.pie(data, names="canal de venda", title="15. Distribuição dos Canais de Venda")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico16', methods=['GET'])
def grafico16():
    fig = px.bar(data.groupby('tipo de envio').sum(numeric_only=True).reset_index(), x="tipo de envio", y="quantidade comprada", title="16. Quantidade Comprada por Tipo de Envio")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico17', methods=['GET'])
def grafico17():
    fig = px.bar(data.groupby('status de entrega').sum(numeric_only=True).reset_index(), x="status de entrega", y="valor de venda", title="17. Valor Total por Status de Entrega")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico18', methods=['GET'])
def grafico18():
    fig = px.histogram(data, x="status de entrega", title="18. Quantidade de Vendas por Status de Entrega")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico19', methods=['GET'])
def grafico19():
    fig = px.bar(data.groupby('canal de venda').sum(numeric_only=True).reset_index(), x="canal de venda", y="valor de venda", title="19. Comparação de Valor de Venda por Canal de Venda")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

@app.route('/grafico20', methods=['GET'])
def grafico20():
    fig = px.bar(data.groupby('estado do envio').sum(numeric_only=True).reset_index(), x="estado do envio", y="valor de venda", title="20. Valor de Venda por Estado de Envio")
    graph_json = pio.to_json(fig)
    return jsonify(graph_json)

if __name__ == '__main__':
    app.run(debug=True)
