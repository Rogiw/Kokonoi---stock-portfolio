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
            país_empresa = input("Digite o país da empresa (ex: US, BR, JP): ").upper()  
            if país_empresa not in extencoes or país_empresa != 2:  
                print("País não suportado. Use os códigos: BR, US, DE, IN, CN, GB. Tente novamente, pois o dev ficou com preguiça de adicionar mais países.")
                continue
            else:
                return país_empresa
        except:
            print("Tudo certinho")


    while y == True:
        try:
            if país_empresa == "US":
                empresa = input("Digite o ticker da empresa (códigos dos EUA, com dígitos entre 1 e 5): " ).upper()
                if 1 <= len(empresa) <=5:
                    print("Ticker válido para os EUA.")
                    
                    return empresa
                else:
                    print("Ticker inválido para os EUA.")
                    continue
            
            elif país_empresa == "BR":
                empresa = input("Digite o ticker da empresa (códigos da B3): " ).upper() +".SA"
                if 4 <= len(empresa) <=5 and empresa[-1] in ["3","4"]:
                    print("Ticker válido para o Brasil.")
                    return empresa
                else:
                    print("Ticker inválido para o Brasil.")
                    continue
         
            elif país_empresa == "DE":
                empresa = input("Digite o ticker da empresa Alemã: " ).upper() +".DE"
                if len(empresa) ==6:
                    print("Ticker válido para a Alemanha.")
                    return empresa
                else:
                    print("Ticker inválido para a Alemanha.")
                    continue
    
            elif país_empresa == "IN":
                empresa = input("Digite o ticker da empresa Indiana: " ).upper() +".NS"
                if 1 <= len(empresa) <=5:
                    print("Ticker válido para para a Índia.")
                    return empresa
                else:
                    print("Ticker inválido para a Índia.")
                    continue
 
            elif país_empresa == "GB":
                empresa = input("Digite o ticker da empresa Inglesa (Reino Unido): " ).upper() +".L"
                if 1 <= len(empresa) <=5:
                    print("Ticker válido para o Reino Unido.")
                    return empresa
                else:
                    print("Ticker inválido para o Reino Unido.")
                    continue
            
            
        except:
            print("Wrong input, please try again.")
    
    Ticker = empresa + extencoes[país_empresa]
    
    return Ticker

def obter_dados_financeiros(empresa, início, fim):
    dados = yf.Ticker(empresa).history(start=início, end=fim)
    dados_anuais = {}
    for ano in range(início, fim):
        dados = yf.Ticker(empresa)
        balanço = dados.balance_sheet
        lucro_perda = dados.financials
        fluxo_caixa = dados.cashflow
        dados_anuais[ano] = (balanço, lucro_perda, fluxo_caixa)
    return balanço, lucro_perda, fluxo_caixa  
    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#main variables
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

obter_Ticker("us")


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#download stock data
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
empresa = obter_Ticker()
print(empresa)
data = yf.Ticker(empresa)
print(data)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#explore data
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#visualize data
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------


