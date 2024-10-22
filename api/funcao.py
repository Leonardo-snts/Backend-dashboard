import plotly.express as px
import plotly.io as pio
import pandas as pd

# Função para carregar os daos da tabela csv
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