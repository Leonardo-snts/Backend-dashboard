import csv
from random import choice, uniform, randint
from datetime import datetime

# Funções auxiliares
def random_date():
    return datetime(2024, randint(1, 12), randint(1, 28)).strftime('%Y-%m-%d')

def random_price(base_price, margin=0.2):
    return round(base_price * (1 + uniform(0.01, margin)), 2)

# Categorias e produtos
categories = {
    "casa": ["sofá", "cadeira", "mesa", "cama"],
    "eletronico": ["smartphone", "televisão", "notebook", "tablet"],
    "cozinha": ["liquidificador", "batedeira", "fogão", "geladeira"],
    "roupa": ["camiseta", "calça", "casaco", "meias"],
    "ferramentas": ["chave de fenda", "martelo", "serra elétrica", "furadeira"]
}

stores = ["Loja A", "Loja B", "Loja C"]

# Moedas e cidades
locations_brl = [
    {"city": "São Paulo", "state": "SP", "country": "Brasil", "lat": -23.5505, "long": -46.6333},
    {"city": "Rio de Janeiro", "state": "RJ", "country": "Brasil", "lat": -22.9068, "long": -43.1729},
    {"city": "Curitiba", "state": "PR", "country": "Brasil", "lat": -25.4284, "long": -49.2733},
]
locations_usd = [
    {"city": "Nova York", "state": "NY", "country": "EUA", "lat": 40.7128, "long": -74.0060},
    {"city": "Los Angeles", "state": "CA", "country": "EUA", "lat": 34.0522, "long": -118.2437},
]
locations_eur = [
    {"city": "Berlim", "state": "BE", "country": "Alemanha", "lat": 52.5200, "long": 13.4050},
    {"city": "Paris", "state": "IL", "country": "França", "lat": 48.8566, "long": 2.3522},
]

shipping_types = ["padrão", "expressa", "transportadora própria"]
sales_channels = ["online", "loja", "empresarial"]

currencies = {
    "BRL": locations_brl,
    "USD": locations_usd,
    "EUR": locations_eur
}

def gerar_dados_distribuidora(num_rows=50, output_file="data/dados_dash.csv"):
    rows = []
    for i in range(1, num_rows + 1):
        category = choice(list(categories.keys()))
        product = choice(categories[category])
        purchase_price = round(uniform(10, 1000), 2)
        selling_price = random_price(purchase_price)
        status = choice(["enviado", "pendente", "cancelado"])
        store = choice(stores)
        date = random_date()
        quantity = randint(1, 100)
        currency = choice(list(currencies.keys()))
        location = choice(currencies[currency])
        shipping_type = choice(shipping_types)
        sales_channel = choice(sales_channels)

        other_store = choice([s for s in stores if s != store])
        store_prices = {
            "distribuidora": selling_price,
            store: random_price(selling_price, margin=0.1),
            other_store: random_price(selling_price, margin=0.1)
        }
        
        rows.append([
            i, category, product, selling_price, purchase_price, status, store, 
            date, quantity, currency, location["city"], location["state"], 
            location["country"], location["lat"], location["long"], 
            shipping_type, sales_channel, store_prices["distribuidora"], 
            store_prices[store], store_prices[other_store]
        ])
    
    header = [
        "id do produto", "tipo do produto", "produto", "valor de venda", "valor de compra", 
        "status de entrega", "loja que comprou", "data da venda", "quantidade comprada", 
        "moeda usada", "cidade do envio", "estado do envio", "pais do envio", 
        "latitude", "longitude", "tipo de envio", "canal de venda", 
        "preço distribuidora", "preço loja 1", "preço loja 2"
    ]
    
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

# Executar a função
gerar_dados_distribuidora(output_file="data/dados_dash.csv")
print('Dados gerados com sucesso e salvo em data/dados_dash.csv')
