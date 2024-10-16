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

# Gráfico de produtos por Status
@app.route('/api/produtos-status', methods=['GET'])
def get_produtos_status ():
    amazon_sales, _, _, _, _ = load_data()
    status_counts = amazon_sales['Status'].value_counts()
    total = status_counts.sum()
    status_percentages = (status_counts / total) *100
    data = status_percentages.reset_index().rename(columns={'index':'Status', 'Status': 'Percentage'})
    return jsonify(data.to_dict(orient="records"))

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
@app.route('/api/weight-vs-qty', methods=['GET'])
def get_weight_vs_qty():
    #amazon_sales, _, may_2022, _, _ = load_data()
    
    # Fazer a junção entre amazon_sales e may_2022 na coluna 'SKU'
    # merged_data = pd.merge(amazon_sales[['SKU', 'Qty']], may_2022[['SKU', 'Weight']], on='SKU', how='inner')
    
    # Agrupar pelos valores de peso e somar a quantidade
    # data = merged_data.groupby('Weight')['Qty'].sum().reset_index()
    
    amazon_sales = pd.read_csv('data/Amazon Sale Report.csv')
    may_2022 = pd.read_csv('data/May-2022.csv')

    amazon_sales['Source'] = 'Amazon Sales'
    may_2022['Source'] = 'May-2022'

    combined_data = pd.concat([amazon_sales['Qty'], may_2022['Weight']], ignore_index=True)
    combined_data.to_csv('data/combined_data.csv')
    comb_data = pd.read_csv('data/combined_data.csv')

    data = comb_data[['Qty', 'Weight']]
    
    return jsonify(data.to_dict(orient="records"))

# 6. Produtos com Maior Estoque
@app.route('/api/top-stock', methods=['GET'])
def get_top_stock():
    _, _, expenses, _, _ = load_data()
    data = expenses[['SKU', 'Stock']].groupby('SKU').sum().reset_index()
    return jsonify(data.to_dict(orient="records"))

# 7. Vendas por Estilo ao Longo do Tempo
@app.route('/api/sales-by-style-over-time', methods=['GET'])
def get_sales_by_style_over_time():
    amazon_sales, _, _, _, _ = load_data()
    data = amazon_sales.groupby(['Date', 'Style'])['Qty'].sum().reset_index()
    return jsonify(data.to_dict(orient="records"))

# 8. Comparação de Preço Original vs Final
@app.route('/api/price-original-vs-final', methods=['GET'])
def get_price_original_vs_final():
    amazon_sales, _, _, _, _ = load_data()
    data = amazon_sales[['SKU', 'MRP Old', 'Final MRP']].groupby('SKU').mean().reset_index()
    return jsonify(data.to_dict(orient="records"))

# 9. Vendas B2B vs Outros Canais
@app.route('/api/sales-b2b', methods=['GET'])
def get_sales_b2b():
    amazon_sales, _, _, _, _ = load_data()
    data = amazon_sales.groupby('sales chanel')['Amount'].sum().reset_index()
    return jsonify(data.to_dict(orient="records"))

# 10. Comparação de Preços entre Plataformas
@app.route('/api/platform-price-comparison', methods=['GET'])
def get_platform_price_comparison():
    _, warehouse_comparison, _, _, _ = load_data()
    data = warehouse_comparison[['Sku', 'Amazon MRP', 'Flipkart MRP', 'Paytm MRP', 'Snapdeal MRP']].dropna()
    return jsonify(data.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)
