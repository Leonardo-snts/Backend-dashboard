from flask import jsonify, Blueprint
import pandas as pd
from api.funcao import data
from flask_cors import cross_origin
import numpy as np

api = Blueprint('api', __name__)

@api.route('/grafico1', methods=['GET'])
def grafico1():
    product_count = data['tipo do produto'].value_counts().reset_index()
    product_count.columns = ['tipo_do_produto', 'contagem']

    return jsonify(product_count.to_dict(orient="records"))

@api.route('/grafico2', methods=['GET'])
def grafico2():
    sales_distribution = data['loja que comprou'].value_counts().reset_index()
    sales_distribution.columns = ['loja', 'contagem']
    return jsonify(sales_distribution.to_dict(orient="records"))

@api.route('/grafico3', methods=['GET'])
def grafico3():
    sales_by_product_type = data.groupby('tipo do produto')['valor de venda'].sum().reset_index()
    sales_by_product_type.columns = ['tipo_do_produto', 'valor_total_venda']
    return jsonify(sales_by_product_type.to_dict(orient="records"))

@api.route('/grafico4', methods=['GET'])
def grafico4():
    purchase_vs_sale = data[['valor de compra', 'valor de venda', 'tipo do produto']]
    return jsonify(purchase_vs_sale.to_dict(orient="records"))

@api.route('/grafico5', methods=['GET'])
def grafico5():
    quantity_by_store = data.groupby('loja que comprou')['quantidade comprada'].sum().reset_index()
    quantity_by_store.columns = ['loja', 'quantidade_total']
    return jsonify(quantity_by_store.to_dict(orient="records"))

@api.route('/grafico6', methods=['GET'])
def grafico6():
    shipping_types = data['tipo de envio'].value_counts().reset_index()
    shipping_types.columns = ['tipo_envio', 'contagem']
    return jsonify(shipping_types.to_dict(orient="records"))

@api.route('/grafico7', methods=['GET'])
def grafico7():
    delivery_status_by_store = data.groupby(['loja que comprou', 'status de entrega']).size().reset_index(name='contagem')
    return jsonify(delivery_status_by_store.to_dict(orient="records"))

@api.route('/grafico8', methods=['GET'])
def grafico8():
    quantity_by_currency = data.groupby('moeda usada')['quantidade comprada'].sum().reset_index()
    quantity_by_currency.columns = ['moeda', 'quantidade_total']
    return jsonify(quantity_by_currency.to_dict(orient="records"))

@api.route('/grafico9', methods=['GET'])
def grafico9():
    sales_by_currency = data.groupby('moeda usada')['valor de venda'].sum().reset_index()
    sales_by_currency.columns = ['moeda', 'valor_total_venda']
    return jsonify(sales_by_currency.to_dict(orient="records"))

@api.route('/grafico10', methods=['GET'])
def grafico10():
    # Selecionar as colunas de interesse
    colunas = ["preço distribuidora", "preço loja 1", "preço loja 2"]
    
    # Construir uma lista de dicionários com o formato desejado
    response_data = [
        {"loja": coluna, "valor": data[coluna].mean()} for coluna in colunas
    ]
    
    # Retornar a resposta no formato JSON
    return jsonify(response_data)

@api.route('/grafico11', methods=['GET'])
def grafico11():
    sales_by_city = data.groupby('cidade do envio')['valor de venda'].sum().reset_index()
    sales_by_city.columns = ['cidade', 'valor_total_venda']
    return jsonify(sales_by_city.to_dict(orient="records"))

@api.route('/grafico12', methods=['GET'])
def grafico12():
    avg_sales_by_product_type = data.groupby('tipo do produto')['valor de venda'].mean().reset_index()
    avg_sales_by_product_type.columns = ['tipo_do_produto', 'media_valor_venda']
    return jsonify(avg_sales_by_product_type.to_dict(orient="records"))

@api.route('/grafico13', methods=['GET'])
def grafico13():
    avg_purchase_by_product_type = data.groupby('tipo do produto')['valor de compra'].mean().reset_index()
    avg_purchase_by_product_type.columns = ['tipo_do_produto', 'media_valor_compra']
    return jsonify(avg_purchase_by_product_type.to_dict(orient="records"))

@api.route('/grafico14', methods=['GET'])
def grafico14():
    data['mes'] = pd.to_datetime(data['data da venda']).dt.month
    purchases_by_month = data.groupby('mes')['quantidade comprada'].sum().reset_index()
    purchases_by_month.columns = ['mes', 'quantidade_total']
    return jsonify(purchases_by_month.to_dict(orient="records"))

@api.route('/grafico15', methods=['GET'])
def grafico15():
    sales_channel_distribution = data['canal de venda'].value_counts().reset_index()
    sales_channel_distribution.columns = ['canal_venda', 'contagem']
    return jsonify(sales_channel_distribution.to_dict(orient="records"))

@api.route('/grafico16', methods=['GET'])
def grafico16():
    quantity_by_shipping_type = data.groupby('tipo de envio')['quantidade comprada'].sum().reset_index()
    quantity_by_shipping_type.columns = ['tipo_envio', 'quantidade_total']
    return jsonify(quantity_by_shipping_type.to_dict(orient="records"))

@api.route('/grafico17', methods=['GET'])
def grafico17():
    sales_by_delivery_status = data.groupby('status de entrega')['valor de venda'].sum().reset_index()
    sales_by_delivery_status.columns = ['status_entrega', 'valor_total_venda']
    return jsonify(sales_by_delivery_status.to_dict(orient="records"))

@api.route('/grafico18', methods=['GET'])
def grafico18():
    sales_count_by_delivery_status = data['status de entrega'].value_counts().reset_index()
    sales_count_by_delivery_status.columns = ['status_entrega', 'contagem']
    return jsonify(sales_count_by_delivery_status.to_dict(orient="records"))

@api.route('/grafico19', methods=['GET'])
def grafico19():
    sales_by_sales_channel = data.groupby('canal de venda')['valor de venda'].sum().reset_index()
    sales_by_sales_channel.columns = ['canal_venda', 'valor_total_venda']
    return jsonify(sales_by_sales_channel.to_dict(orient="records"))

@api.route('/grafico20', methods=['GET'])
def grafico20():
    sales_by_shipping_state = data.groupby('estado do envio')['valor de venda'].sum().reset_index()
    sales_by_shipping_state.columns = ['estado_envio', 'valor_total_venda']
    return jsonify(sales_by_shipping_state.to_dict(orient="records"))

@api.route('/grafico21')
def sales_heatmap():
    city_data = data.groupby(
        ['cidade do envio', 'latitude', 'longitude']
    )['quantidade comprada'].sum().reset_index()
    
    # Agrupa por país, ignorando cidades e estados
    country_data = data.groupby('pais do envio')['quantidade comprada'].sum().reset_index()
    country_data.rename(columns={'pais do envio': 'country'}, inplace=True)

    # Converte para JSON com diferentes agrupamentos
    result = {
        "cities": city_data.to_dict(orient="records"),
        "countries": country_data.to_dict(orient="records")
    }

    return jsonify(result)