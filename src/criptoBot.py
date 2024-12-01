import ccxt
import json
import time
from datetime import datetime
from api import app

binance_credentials = {}
binance = ccxt.binance()

# Função para ler a chave da API e o segredo de um arquivo JSON
def ler_api_keys(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON de chaves: {e}")
        return None

# configurar client binance
def binance_config():
    binance = ccxt.binance()

# Função para carregar configurações de moedas
def carregar_moedas():
    with open('moedas.json', 'r') as file:
        return json.load(file)


# Função para salvar criptoData de transação por moeda
def salvar_transacao(moeda, transacao):
    with open(f'{moeda}.json', 'a') as file:
        json.dump(transacao, file)
        file.write('\n')


# Função para registrar logs diários
def salvar_log(mensagem):
    log_filename = datetime.now().strftime('%Y%m%d') + ".txt"
    with open(log_filename, 'a') as log_file:
        log_file.write(mensagem + "\n")


# Obter o preço atual de uma moeda na Binance
def obter_preco(moeda):
    ticker = binance.fetch_ticker(moeda)
    print(f'{moeda}: {ticker}')
    return ticker['last']


# Verificar cotações
def verificar_cotacoes(config, moeda_data):
    print(moeda_data)
    preco_atual = obter_preco(moeda_data['simbolo'])
    print(datetime.now(),preco_atual)

# Monitorar preços a cada minuto
def monitorar_moedas():
    config = carregar_moedas()
    ler_api_keys('binance.json')
    binance_config()

    print(config)

    while True:
        for moeda_data in config['moedas']:
            verificar_cotacoes(config, moeda_data)

        time.sleep(1)


if __name__ == "__main__":
    monitorar_moedas()
    app.run(debug=True, host="127.0.0.1", port=5000)
