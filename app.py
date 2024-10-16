# import dotenv
# import os

# dotenv.load_dotenv(dotenv.find_dotenv())

# username = os.getenv("username")
# password = os.getenv("password")


# print(username)
# print(password)


from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita o CORS para permitir que o frontend acesse a API

# Função para carregar os dados
def load_data():
    amazon_sales = pd.read_csv('data/Amazon Sale Report.csv')
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
    data = may_2022[['Sku', 'Amazon MRP', 'Flipkart MRP', 'Myntra MRP']]
    return jsonify(data.to_dict(orient="records"))

# 5. Peso vs Quantidade Vendida
# @app.route('/api/weight-vs-qty', methods=['GET'])
# def get_weight_vs_qty():
#     # Carregar os dados
#     amazon_sales = pd.read_csv('data/Amazon Sale Report.csv')
#     may_2022 = pd.read_csv('data/May-2022.csv')

#     # Verificar se ambos os arquivos têm o mesmo número de linhas
#     min_length = min(len(amazon_sales), len(may_2022))

#     # Pegar a quantidade da amazon_sales e o peso do may_2022 até o comprimento mínimo
#     qty_data = amazon_sales['Qty'][:min_length]
#     weight_data = may_2022['Weight'][:min_length]

#     # Criar um novo DataFrame com ambas as colunas
#     combined_data = pd.DataFrame({
#         'Qty': qty_data,
#         'Weight': weight_data
#     })

#     # Converter os dados para JSON e retornar a resposta
#     return jsonify(combined_data.to_dict(orient="records"))

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
@app.route('/api/sales-by-style-over-time', methods=['GET'])
def get_sales_by_style_over_time():
    amazon_sales, _, _, _, _ = load_data()
    data = amazon_sales.groupby(['Date', 'Style'])['Qty'].sum().reset_index()
    return jsonify(data.to_dict(orient="records"))

# 7. Comparação de Preço Original vs Final
@app.route('/api/price-original-vs-final', methods=['GET'])
def get_price_original_vs_final():
    amazon_sales, _, _, _, _ = load_data()
    data = amazon_sales[['SKU', 'MRP Old', 'Final MRP']].groupby('SKU').mean().reset_index()
    return jsonify(data.to_dict(orient="records"))

# 8. Vendas B2B vs Outros Canais
@app.route('/api/sales-b2b', methods=['GET'])
def get_sales_b2b():
    amazon_sales, _, _, _, _ = load_data()
    data = amazon_sales.groupby('sales chanel')['Amount'].sum().reset_index()
    return jsonify(data.to_dict(orient="records"))

# 9. Comparação de Preços entre Plataformas
@app.route('/api/platform-price-comparison', methods=['GET'])
def get_platform_price_comparison():
    _, warehouse_comparison, _, _, _ = load_data()
    data = warehouse_comparison[['Sku', 'Amazon MRP', 'Flipkart MRP', 'Paytm MRP', 'Snapdeal MRP']].dropna()
    return jsonify(data.to_dict(orient="records"))

# 10. Gráfico de produtos por Status
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
