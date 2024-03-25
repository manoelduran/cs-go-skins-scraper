from playwright.sync_api import  sync_playwright
import csv
import json


def run_crawler():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # URL da API
        url = "https://api.dashskins.gg/v1/item?pageSize=2000&maxPriceBRL=2000&minPriceBRL=150&exterior=Factory%20New,Minimal%20Wear,Field-Tested&sort=discount-desc"

        # Navega para a URL
        page.goto(url)

        # Espera a resposta da requisição
        page.wait_for_load_state("networkidle")

        # Obtém o conteúdo da resposta
        response = page.content()

        # Fecha o navegador
        browser.close()

        return response

# Executa o crawler e imprime a resposta
response_content = run_crawler()


def extract_data(response_content):
    # Encontra o início da chave "page" na resposta
    start_index = response_content.find('{"page":')
    
    # Se a chave "page" não for encontrada, retorna uma lista vazia
    if start_index == -1:
        print("Erro: Objeto 'page' não encontrado na resposta.")
        return []
    
    # Encontra a posição do último fechamento de chaves '}' após o início da chave "page"
    end_index = response_content.rfind('}', start_index)
    
    # Extrai o conteúdo dentro da chave "page"
    page_data_str = response_content[start_index:end_index + 1]

    # Converte o conteúdo para um dicionário Python
    response_data = json.loads(page_data_str)
    
    # Lista para armazenar os dados extraídos
    extracted_data = []
    
    # Itera sobre cada item na resposta e extrai os dados necessários
    for item in response_data['page']:
        item_data = {
            'id': item['id'],
            'marketHashName': item['marketHashName'],
            'priceBRL': item['priceBRL'],
            'steamPriceUSD': item['steamPriceUSD'],
            'float': item['float'],
            'rarity': item['rarity'],

        }
        extracted_data.append(item_data)
    
    return extracted_data
def write_to_csv(data):
    # Define os nomes das colunas do CSV
    fieldnames = ['id', 'marketHashName', 'priceBRL', 'steamPriceUSD', 'float', 'rarity']
    
    # Nome do arquivo CSV
    csv_filename = 'dados_items.csv'
    
    # Escreve os dados no arquivo CSV
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Escreve o cabeçalho
        writer.writeheader()
        
        # Escreve os dados de cada item
        for item in data:
            writer.writerow(item)

# Extrai os dados da resposta
extracted_data = extract_data(response_content)

# Escreve os dados extraídos em um arquivo CSV
write_to_csv(extracted_data)

print("Arquivo CSV criado com sucesso!")
