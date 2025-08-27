#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#import libraries
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf #this is for downloading stock data


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#functions
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
"""Margem Bruta = Resultado Bruto / Receita Líquida de Vendas e/ou Serviços Mede a eficiência produtiva. 
Margem Líquida = Lucro/Prejuízo do Período / Receita Líquida de Vendas e/ou Serviços Mede a lucratividade final. 
ROE (Return on Equity) = Lucro/Prejuízo do Período / Patrimônio Líquido Mede a rentabilidade sobre o capital próprio. Se não tiver Patrimônio Líquido, precisa adicioná-lo. 
ROA (Return on Assets) = Lucro/Prejuízo do Período / Ativo Total Mede a eficiência no uso dos ativos. 
Índice de Endividamento = (Empréstimos e Financiamentos_1 + Empréstimos e Financiamentos) / Ativo Total Mede a alavancagem da empresa. 
Turnover de Contas a Receber = Receita Líquida de Vendas e/ou Serviços / Contas a Receber_1 Mede quanto vezes a empresa cobra suas contas por ano. Quanto maior, melhor. 
FCO / Receita Líquida = Fluxo de Caixa Operacional / Receita Líquida de Vendas e/ou Serviços Mede a qualidade da receita (quanto se transforma em caixa). 
FCO / Lucro Líquido = Fluxo de Caixa Operacional / Lucro/Prejuízo do Período Mede a qualidade do lucro."""

"""Brasil (B3) → .SA
    EUA (NYSE/NASDAQ) → não precisa de extensão, ex: AAPL
    Canadá (TSX) → .TO
    Reino Unido (LSE) → .L
    Alemanha (XETRA) → .DE"""

"""y = True
    while y == True:
    x = input("Enter a number:")
    try:
    x = float(x);
    y = False
        except:
    print("Wrong input, please try again.")"""

def obter_Ticker(país_empresa):

    país_empresa = país_empresa.upper()
    extencoes = {
        "BR": ".SA",
        "US": "",
        "DE": ".DE",
        "IN": ".NS",
        "CN": ".SS",
        "GB": ".L"
    }
    y = True
    while y == True:
        try:
            if país_empresa == "US":
                empresa = input("Digite o ticker da empresa (códigos dos EUA, com dígitos entre 1 e 5): " ).upper()
                if 1 <= len(empresa) <=5:
                    print(f"Ticker,{empresa}, válido para os EUA.")
                    
                    return empresa
                else:
                    print("Ticker inválido para os EUA.")
                    continue
            
            elif país_empresa == "BR":
                empresa = input("Digite o ticker da empresa (códigos da B3): " ).upper() 
                if 4 <= len(empresa) <=5 and empresa[-1] in ["3","4"]:
                    print(f"Ticker, {empresa}, válido para o Brasil.")
                    empresa += ".SA"
                    return empresa
                else:
                    print(f"Ticker, {empresa}, inválido para o Brasil.")
                    continue
         
            elif país_empresa == "DE":
                empresa = input("Digite o ticker da empresa Alemã: " ).upper()
                if len(empresa) ==6:
                    print(f"Ticker, {empresa}, válido para a Alemanha.")
                    empresa += ".DE"
                    return empresa
                else:
                    print(f"Ticker, {empresa}, inválido para a Alemanha.")
                    continue
    
            elif país_empresa == "IN":
                empresa = input("Digite o ticker da empresa Indiana: " ).upper() 
                if 1 <= len(empresa) <=5:
                    print(f"Ticker, {empresa}, válido para para a Índia.")
                    empresa += ".NS"
                    return empresa
                else:
                    print(f"Ticker, {empresa}, inválido para a Índia.")
                    continue
 
            elif país_empresa == "GB":
                empresa = input("Digite o ticker da empresa Inglesa (Reino Unido): " ).upper() 
                if 1 <= len(empresa) <=5:
                    print(f"Ticker, {empresa}, válido  válido para o Reino Unido.")
                    empresa += ".L"
                    return empresa
                else:
                    print(f"Ticker, {empresa}, inválido para o Reino Unido.")
                    continue
            else:  
                print("País não suportado. Use os códigos: BR, US, DE, IN, CN, GB. Tente novamente, pois o dev ficou com preguiça de adicionar mais países.")
                país_empresa = input("Digite o país da empresa (ex: US, BR, JP): ").upper()
                continue
             
        except:
            print("Wrong input, please try again.") 
    
    Ticker = empresa + extencoes[país_empresa]
    
    return Ticker

def obter_dados_financeiros(empresa):
    print("Obterndo os dados financeiros...")

    #acessar a função de mudança de datas para período personalizado
    dates_to_periodo()

    #acessando efetivamente os dados financeiros
    dados = yf.Ticker(empresa).history(start=datas["início"],end=datas["fim"])
    dados_anuais = {}
    for ano in range('2012-12-31','2020-12-31'):
        balanço = dados.balance_sheet
        lucro_perda = dados.financials
        fluxo_caixa = dados.cashflow
        dados_anuais[ano] = {
            'balanço': balanço,
            'lucro_perda': lucro_perda,
            'fluxo_caixa': fluxo_caixa
        }
    return dados_anuais, dados  

def dates_to_periodo():
    
    periodo_dates = input("Digite o período desejado para análise financeira (formato: YYYY-MM-DD, YYYY-MM-DD): ")

    y = True
    while y == True:    
        try:
            data = periodo_dates.split(",")
            start = data[0].strip()
            end = data[1].strip()
            start_data_valid = pd.to_datetime(start, format='%Y-%m-%d') #posso usar essas datas em um futuro, quando precisar dos dias e do mês
            end_data_valid = pd.to_datetime(end, format='%Y-%m-%d')
            y = False
        except:
            print("Formato de data inválido. Use o formato: YYYY-MM-DD, YYYY-MM-DD. Tente novamente.")
            print("Por favor, selecione realmente dadas válidas, ano-mês-dia com uma vírgula (\",\") separando as duas datas.")
            periodo_dates = input("Digite o período desejado para análise financeira (formato: YYYY-MM-DD, YYYY-MM-DD): ")
            continue

    anos = {"início":start, "fim":end}
    start_anual = pd.to_datetime(start, format='%Y-%m-%d').year
    end_anual = pd.to_datetime(end, format='%Y-%m-%d').year
    for ano in anos:
        anos[ano] = pd.to_datetime(anos[ano], format='%Y-%m-%d').year
    print(data)
    datas_periodo_anual= abs(anos['fim'] - anos['início'])
    print(datas_periodo_anual)
    return datas_periodo_anual, start_anual, end_anual

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#main variables
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
tela_inicial = print("Analisador Financeiro de Empresas - v0.1")
país_empresa = input("Digite o país da empresa (ex: US, BR, JP): ").upper()
empresa = obter_Ticker(país_empresa)

dados = obter_dados_financeiros(empresa)
print(type(dados))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#download stock data
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#print(empresa)
#data = yf.Ticker(empresa)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#explore data
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#visualize data
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
display()

