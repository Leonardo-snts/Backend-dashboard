from flask import Flask, jsonify, Response
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def load_data():
    return pd.read_csv("data/dados_dash.csv")

data = load_data()

# Função para criar o gráfico baseado na seleção
def create_heatmap(df, level):
    if level == 'cidade':
        fig = px.scatter_geo(
            df,
            lat='latitude',
            lon='longitude',
            size='quantidade comprada',
            color='quantidade comprada',
            hover_name='cidade do envio',
            title="Mapa de Calor por Cidade",
            projection="natural earth"
        )
    elif level == 'estado':
        fig = px.scatter_geo(
            df,
            locations='estado do envio',
            locationmode='USA-states',  # Usa os estados dos EUA, mas ajusta para outros países
            size='quantidade comprada',
            color='quantidade comprada',
            hover_name='estado do envio',
            title="Mapa de Calor por Estado",
            projection="natural earth"
        )
    else:  # País
        fig = px.scatter_geo(
            df,
            locations='pais do envio',
            locationmode='country names',
            size='quantidade comprada',
            color='quantidade comprada',
            hover_name='pais do envio',
            title="Mapa de Calor por País",
            projection="natural earth"
        )
    
    fig.update_geos(showcountries=True, showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="lightgray")
    return fig

@app.route('/grafico21', methods=['GET'])
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
    return Response(response=graph_json, status=200, mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True)