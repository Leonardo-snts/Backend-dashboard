from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
from opencage.geocoder import OpenCageGeocode
import dotenv
import os

app = Flask(__name__)
CORS(app)  # Habilita o CORS para permitir que o frontend acesse a API

# Função para carregar os dados
def load_data():
    amazon_sales = pd.read_csv('data/Amazon Sale Report.csv', low_memory=False)
    international_sale = pd.read_csv('data/International sale Report.csv')
    may_2022 = pd.read_csv('data/May-2022.csv')
    march_2021 = pd.read_csv('data/P  L March 2021.csv')
    sale_report = pd.read_csv('data/Sale Report.csv')
    # warehouse_comparison = pd.read_csv('data/Cloud Warehouse Compersion Chart.csv')
    # expenses = pd.read_csv('data/Expense IIGF.csv')
    return amazon_sales, international_sale, may_2022, march_2021, sale_report #,warehouse_comparison, expenses

# 1. Vendas por Estado (Amazon)
@app.route('/api/amazon-sales-by-state', methods=['GET'])
def get_amazon_sales_by_state():
    amazon_sales, _, _, _, _ = load_data()
    data = amazon_sales.groupby('ship-state')['Amount'].sum().reset_index()
    return jsonify(data.to_dict(orient="records"))

# 2. Distribuição de Vendas por Categoria
@app.route('/api/sales-by-category', methods=['GET'])
def get_sales_by_category():
    amazon_sales, _, _, _, _ = load_data()
    data = amazon_sales.groupby('Category')['Amount'].sum().reset_index()
    return jsonify(data.to_dict(orient="records"))

# 3. Vendas ao Longo do Tempo
@app.route('/api/sales-over-time', methods=['GET'])
def get_sales_over_time():
    amazon_sales, _, _, _, _ = load_data()
    data = amazon_sales.groupby('Date')['Amount'].sum().reset_index()
    return jsonify(data.to_dict(orient="records"))

# 4. Comparação de Preços MRP (Amazon, Flipkart, Myntra)
@app.route('/api/price-comparison', methods=['GET'])
def get_price_comparison():
    _, _, may_2022, _, _ = load_data()
    data = may_2022[['Sku', 'Ajio MRP','Amazon FBA MRP', 'Limeroad MRP', 'Paytm MRP', 'Snapdeal MRP','Amazon MRP', 'Flipkart MRP', 'Myntra MRP']]
    #Ajio MRP,Amazon MRP,Amazon FBA MRP,Flipkart MRP,Limeroad MRP,Myntra MRP,Paytm MRP,Snapdeal MRP
    return jsonify(data.to_dict(orient="records"))

# 5. Produtos com Maior Estoque
@app.route('/api/top-stock', methods=['GET'])
def get_top_stock():
    # Carregar os dados do sale_report
    _, _, _, _, sale_report = load_data()

    # Agrupar por 'Category' e somar o 'Stock' correspondente
    category_stock = sale_report.groupby('Category')['Stock'].sum().reset_index()

    # Renomear as colunas para uma representação mais clara
    category_stock = category_stock.rename(columns={'Category': 'Categoria', 'Stock': 'Estoque'})

    # Retornar os dados em formato JSON
    return jsonify(category_stock.to_dict(orient="records"))

# 6. Vendas por Estilo ao Longo do Tempo
@app.route('/api/sales-qty-over-time', methods=['GET'])
def get_sales_by_time():
    # Parâmetro para definir o agrupamento (dia, mês ou ano)
    group_by = request.args.get('group_by', 'D')  # O padrão será 'D' (dia)

    amazon_sales, _, _, _, _ = load_data()

    # Tentar converter a coluna 'Date' para datetime e mostrar erros de conversão
    amazon_sales['Date'] = pd.to_datetime(amazon_sales['Date'], errors='coerce')

    # Exibir dados inválidos para debug
    # invalid_dates = amazon_sales[amazon_sales['Date'].isna()]
    # print(f"Linhas com datas inválidas: {len(invalid_dates)}")

    # Remover linhas com datas inválidas (mantendo essa parte para o fluxo normal)
    amazon_sales = amazon_sales.dropna(subset=['Date'])

    # Definir a frequência de agrupamento com base no parâmetro
    if group_by == 'D':  # Dia
        freq = 'D'
        output_format = '%Y-%m-%d'
    elif group_by == 'Y':  # Ano
        freq = 'YE'
        output_format = '%Y'
    else:  # Mês (padrão)
        freq = 'ME'
        output_format = '%Y-%m'

    # Agrupar por data (dia, mês ou ano) somando as quantidades vendidas ('Qty')
    sales_by_time = amazon_sales.groupby(pd.Grouper(key='Date', freq=freq))['Qty'].sum().reset_index()

    # Renomear a coluna 'Date' para 'Time' e formatar conforme necessário
    sales_by_time['Time'] = sales_by_time['Date'].dt.strftime(output_format)

    # Remover a coluna 'Date' e manter apenas 'Time' e 'Qty'
    sales_by_time = sales_by_time[['Time', 'Qty']]

    # Retornar os dados como JSON
    return jsonify(sales_by_time.to_dict(orient="records"))

# 7. Comparação de Preço Original vs Final
@app.route('/api/price-original-vs-final', methods=['GET'])
def get_price_original_vs_final():
    _, _, may_2022, _, _ = load_data()
    
    # Selecionar as colunas necessárias
    data = may_2022[['Sku', 'MRP Old', 'Final MRP Old']].copy()  # Usar .copy() para evitar problemas de "view" vs "copy"
    
    # Converter as colunas 'MRP Old' e 'Final MRP Old' para numérico com .loc[]
    data.loc[:, 'MRP Old'] = pd.to_numeric(data['MRP Old'], errors='coerce')
    data.loc[:, 'Final MRP Old'] = pd.to_numeric(data['Final MRP Old'], errors='coerce')

    # Remover linhas com valores NaN após a conversão
    data = data.dropna(subset=['MRP Old', 'Final MRP Old'])

    # Calcular a variação de preço (%)
    data['Price Variation (%)'] = ((data['Final MRP Old'] - data['MRP Old']) / data['MRP Old']) * 100

    # Retornar os dados como JSON
    return jsonify(data.to_dict(orient="records"))

# 8. Comparação de Preços entre Plataformas
@app.route('/api/heat-map', methods=['GET'])
def get_heat_map():
    amazon_sales, _, _, _, _ = load_data()

    # gambiarra até trocar os dados
    country_mapping = {
        'IN': 'India',
        # Adicione mais mapeamentos conforme necessário
    }

    # Aplicando a substituição dos códigos
    amazon_sales['ship-country'] = amazon_sales['ship-country'].replace(country_mapping)

    # Agrupando por país e somando as vendas
    data = amazon_sales.groupby('ship-country')['Amount'].sum().reset_index()

    # Convertendo o resultado para um formato apropriado
    return jsonify(data.to_dict(orient="records"))


# 9. Gráfico de produtos por Status
@app.route('/api/produtos-status', methods=['GET'])
def get_produtos_status ():
    amazon_sales, _, _, _, _ = load_data()
    status_counts = amazon_sales['Status'].value_counts()
    total = status_counts.sum()
    status_percentages = (status_counts / total) *100
    data = status_percentages.reset_index().rename(columns={'index':'Status', 'Status': 'Percentage'})
    return jsonify(data.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)
