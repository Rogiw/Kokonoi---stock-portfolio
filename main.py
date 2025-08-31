#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#import libraries
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf #this is for downloading stock data
import requests as r
import os
import zipfile
import io
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS 






#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#FrontEnd
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar_empresa', methods=['GET'])
def buscar_empresa():
    nome = r.args.get('nome', '').lower()
    
    if not nome:
        return jsonify({"erro": "Por favor, informe o nome de uma empresa"})
    
    resultados = [empresa for empresa in EMPRESAS if nome in empresa['nome'].lower()]
    
    if not resultados:
        return jsonify({"mensagem": "Nenhuma empresa encontrada com esse nome"})
    
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)





#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#functions
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#funcoes para calcular metricas de cada empresa









#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#funcoes de busca de dados e algumas ferramentas
def obter_Ticker_yf(país_empresa):

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

def save_to_cache(open_link = None, dict_download = None, extensao = None):
    """Salva dados no cache local"""
    try:
        #aqui quero que salve os arquivos brutos, sem tratar. Por exemplo, vai ter varias empresas misturadas dentro de uma msm planilha. A única divisão vai ser por ano e olhe lá 
        if extensao in  ['zip']:
            with zipfile.ZipFile(io.BytesIO(open_link.content)) as z:
                for zfile in z.namelist():         
                    if not os.path.exists(f'cache/{zfile}'):
                        print("Arquvivo não existe no cache, baixando...", zfile)
                        z.extract(zfile, "cache")  # extrai todos os arquivos                                                     
                    else:
                        print(f"Arquivo {zfile} já existe no cache.")
                        continue
        #pd_read = getattr(pd, f'read_{zfile.rsplit(".", 1)[-1]}', None)
        #opening = pd_read(f'cache/{zfile}', encoding='latin1', dtype=str, low_memory=False)
        print("Dados salvos no cache com sucesso!")
        
        #aqui eu quero que salve os dados tratados, ou seja, separados por empresa
        #if ticker, arquivo in dict_links.items():


    except Exception as e:
        print(f"Erro ao salvar no cache: {e}")
        return None

def get_cached_data(ticker):
    """Obtém dados do cache local"""
    try:
        filepath = f'cache/{ticker}'
        if os.path.exists(filepath):
            pd_read = getattr(pd, f'read_{ticker.rsplit(".", 1)[-1]}', None)
            opening = pd_read(f'cache/{ticker}', encoding='latin1', dtype=str, low_memory=False, sep=';', usecols=['CNPJ_CIA', 'DENOM_CIA', 'QT_ACAO_TOTAL_CAP_INTEGR'])
            data = opening
            display(data)
            print("Parabens otário, você conseguiu achar o arquivo no cache!")
            return opening
    except Exception as e:
        print(f"Erro ao ler cache: {e}")
    return None

def obter_dados_financeiros_contingência(empresa):
     # 4. Último recurso: usar cache
    print(f"Tentando dados em cache para {ticker}...")
    cached_data = get_cached_data(ticker_lower)
    if cached_data is not None:
        print("Usando dados do cache!")
        return cached_data
    
    # Se tudo falhar
    raise Exception(f"Não foi possível obter dados para {ticker}")

def dict_requests(request):
    url  = request

    #tenta fazer a conexão
    try:
        response = r.get(url, timeout=5)  # espera no máximo 5 segundos
        response.raise_for_status()  # opcional: dispara erro se o status não for 200
        print("Conectou com sucesso!")
    except r.Timeout:
        print("O tempo de espera acabou!")
    except r.RequestException as e:
        print("Erro na requisição:", e)

    soup = BeautifulSoup(response.text, "html.parser")

    # pega todos os links
    links = [a['href'] for a in soup.find_all('a', href=True)]
    link_dict = {}
    for link in links:
        if link.rsplit('.')[-1].lower() in ('zip', 'ZIP', "csv", 'xls'):
            print(f' link válido: {link}')
            link_dict[str(link.rsplit('.', 1)[0])] = link 
    display(link_dict)
    return link_dict
    

def obter_dados_financieiros_cvm(empresa):
    global url_cvm
    url_cvm = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/"  # endereço da pasta para os arquvios da CVM  
    try:
        if os.path.exists('cache'):
            dados = get_cached_data(empresa) 
            print("Usando dados do cache!")
            return dados
        else:
            print("Sem dados em cache, baixando da CVM...")
            dict_linksZip_cvm = dict_requests(url_cvm) 

            for _, link in dict_linksZip_cvm.items():
                with r.get(url_cvm+link, stream=True) as open_link: #aqui ele está abrindo o link do zip
                    open_link.raise_for_status()
                    extensao = link.rsplit('.')[-1].lower()
                    save_to_cache(open_link, dict_linksZip_cvm, extensao)
            return get_cached_data()
    except:
        return print("Erro ao obter dados da CVM.")
    
def obter_dados_financeiros_yf(empresa):
    print("Obterndo os dados financeiros...")

    #acessar a função de mudança de datas para período personalizado
    datas = dates_to_periodo()

    #acessando efetivamente os dados financeiros
    dados = yf.Ticker(empresa)
    dados_financeiros = dados.history(period = str(datas["período"])+"y") #exemplo: "5y" para 5 anos, "1y" para 1 ano, "6mo" para 6 meses, "1d" para 1 dia, "5d" para 5 dias)
    dados_anuais = {}
    for ano in range(datas["início_dt"], datas["fim_dt"] + 1):
        balanço = dados.balance_sheet
        lucro_perda = dados.financials
        fluxo_caixa = dados.cashflow
        dados_anuais[ano] = {
            'balanço': balanço,
            'lucro_perda': lucro_perda,
            'fluxo_caixa': fluxo_caixa
        }
        print(f"Dados financeiros para o ano {ano} obtidos com sucesso.")
        print(dados_anuais[ano], "\n")
    return dados_anuais, dados_financeiros  

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
    print(anos)
    datas_periodo_anual= abs(anos['fim'] - anos['início'])
    print(datas_periodo_anual)
    datas = {
        "início_dt": start_anual,
        "fim_dt": end_anual,
        "período": datas_periodo_anual,
        "anos_list": anos
    }
    return datas
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#classes
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#2008-03-01 to 2025-03-01
class carteira:
    def __init__(self, name)
        self.name = name

class empresa:
  def __init__(self, name, cnpj, ticker, descrição, setor, dados):
    self.name = name
    self.cnpj = cnpj
    self.ticker = ticker
    self.descrição = descrição
    self.setor = setor
    self.dados = dados


    def LiquidezCorrente():
        """Ativo Circulante / Passivo Circulante- Saúde de curto prazo; >1.5 é bom."""
    def DividaLiquida():
        """(Empréstimos CP + LP - Caixa) / EBITDA -	Capacidade de pagar dívida; <3 é saudável."""
    def MargenLiquida():
        """Lucro Líquido / Receita Líquida -	Eficiência em gerar lucro; consistência é key."""
    def roe():
        """ (Return on Assets)	Lucro Líquido / Ativo Total -	Eficiência no uso dos ativos; quanto maior, melhor."""
    def PL():
        """(Preço/Lucro)	Preço da Ação / Lucro por Ação (LPA)	Valuation; compare com média do setor."""
    def PVP():
        """(Preço/Valor Patrimonial)	Preço da Ação / Valor Patrimonial por Ação (VPA)	Valuation; <1 pode ser subvalorizado."""
    def EVEBITDA():
        """Enterprise Value / EBITDA	Valuation ajustado por dívida; menor é melhor."""
    def FCORL():
        """Fluxo de Caixa Operacional / Receita Líquida	Qualidade da receita; >0.2 é bom."""
    def FCOLL():
        """Fluxo de Caixa Operacional / Lucro Líquido	Qualidade do lucro; próximo de 1 ou maior é ideal."""
    def CAGR():
        """Receita (5 anos)	(Receita Ano Atual / Receita Ano Base)^(1/5) - 1	Crescimento sustentável da receita."""






class setor:
    def __init__(self, nome):
        self.nome = nome
        self.empresas = []

    def adicionar_empresa(self, empresa):
        self.empresas.append(empresa)

    def media_setor(self):
        pass
    
    
    #Comparar o df de todas que pegar da cvm que tiver no mesmo setor
    def comparar_empresas(self, empresa):
        media_setor = self.media_setor()
        meida_empresa = empresa.media_lucros()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------    
#Sublicasses para os principais setores da cabeça do dev
class mineração(Setor):
    """Exploração & Produção de Petróleo e Gás, Equipamentos & Serviços de Petróleo"""
    def __init__()
class Materiais(Setor):
    """Produtos Químicos, Materiais de Construção, Contêineres & Embalagens, Metais & Mineração"""
    def __init__()
class Industrias(Setor):
    """Capital Goods, Serviços Comerciais & Profissionais, Transporte"""
    def __init__()
class BensDiscricionários(Setor):
    """Automóveis e Componentes, Bens Duráveis, Hoteleira & Lazer, Mídia & Publicidade, Varejo Discricionário"""
    def __init__()
class BensEssenciais():
    """Produtos de Uso Pessoal, Alimentos, Bebidas & Tabaco, Varejo de Alimentos & Medicamentos"""  
    def __init__()
class Saude():
    """Equipamentos & Serviços de Saúde, Tecnologia & Suprimentos de Saúde, Empresas Farmacêuticas, Biotecnologia"""
    def __init__()
class Financeiro():
    """Bancos, Diversificados Financeiros, Seguradoras, Imobiliário (REITs)"""
    def __init__()
class TI():
    """	Serviços & Software de TI, Hardware & Equipamentos de TI, Semiconductores & Equipamentos"""
    def __init__()
class Comunicacoes():
    """	Serviços de Telecomunicações, Mídia & Entretenimento"""
    def __init__()
class Utilidadaes():
    """	Utilidades Elétricas, Utilidades de Gás, Utilidades de Água"""
    def __init__()
class Imobiliario():
    """Desenvolvimento Imobiliário, Serviços Imobiliários, REITs (diversos tipos)"""
    def __init__()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------       










#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#main variables
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#estruturar as primeiras coisas que quero que faça






tela_inicial = print("Analisador Financeiro de Empresas - v0.1")
país_empresa = input("Digite o país da empresa (ex: US, BR, JP): ").upper()
empresa = obter_Ticker_yf(país_empresa)

dados = obter_dados_financeiros_yf(empresa)
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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#Analysis
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
"""Margem Bruta = Resultado Bruto / Receita Líquida de Vendas e/ou Serviços Mede a eficiência produtiva. 
Margem Líquida = Lucro/Prejuízo do Período / Receita Líquida de Vendas e/ou Serviços Mede a lucratividade final. 
ROE (Return on Equity) = Lucro/Prejuízo do Período / Patrimônio Líquido Mede a rentabilidade sobre o capital próprio. Se não tiver Patrimônio Líquido, precisa adicioná-lo. 
ROA (Return on Assets) = Lucro/Prejuízo do Período / Ativo Total Mede a eficiência no uso dos ativos. 
Índice de Endividamento = (Empréstimos e Financiamentos_1 + Empréstimos e Financiamentos) / Ativo Total Mede a alavancagem da empresa. 
Turnover de Contas a Receber = Receita Líquida de Vendas e/ou Serviços / Contas a Receber_1 Mede quanto vezes a empresa cobra suas contas por ano. Quanto maior, melhor. 
FCO / Receita Líquida = Fluxo de Caixa Operacional / Receita Líquida de Vendas e/ou Serviços Mede a qualidade da receita (quanto se transforma em caixa). 
FCO / Lucro Líquido = Fluxo de Caixa Operacional / Lucro/Prejuízo do Período Mede a qualidade do lucro."""

"""dfp = Demonstrações Financeiras Padronizadas"""

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

""""
------------------exemplo de DRE (Demonstrativo de Resultados)------------------
Ativo Total
Ativo Circulante
Caixa e Equivalentes de Caixa
Aplicações Financeiras
Contas a Receber
Estoques
Ativos Biológicos
Tributos a Recuperar
Despesas Antecipadas
Outros Ativos Circulantes
Ativo Realizável a Longo Prazo
Aplicações Financeiras Avaliadas a Valor Justo
Aplicações Financeiras Avaliadas ao Custo Amortizado
Contas a Receber
Estoques
Ativos Biológicos
Tributos Diferidos
Despesas Antecipadas
Créditos com Partes Relacionadas
Outros Ativos Não Circulantes
Investimentos
Imobilizado
Intangível
Diferido
Passivo Total
Passivo Circulante
Obrigações Sociais e Trabalhistas
Fornecedores
Obrigações Fiscais
Empréstimos e Financiamentos
Passivos com Partes Relacionadas
Dividendos e JCP a Pagar
Outros
Provisões
Passivos sobre Ativos Não-Correntes a Venda e Descontinuados
Passivo Não Circulante
Empréstimos e Financiamentos
Passivos com Partes Relacionadas
Outros
Tributos Diferidos
Adiantamento para Futuro Aumento Capital
Provisões
Passivos sobre Ativos Não-Correntes a Venda e Descontinuados
Lucros e Receitas a Apropriar
Participação dos Acionistas Não Controladores
Patrimônio Líquido
Capital Social Realizado
Reservas de Capital
Reservas de Reavaliação
Reservas de Lucros
Lucros/Prejuízos Acumulados
Ajustes de Avaliação Patrimonial
Ajustes Acumulados de Conversão
Outros Resultados Abrangentes
Adiantamento para Futuro Aumento Capital


------------------exemplo de DRE (Demonstrativo de Resultados)------------------
vou precisar mapear os nomes das contas do B3data para os nomes do DRE
DS_CONTA
Passivo Total
Passivo Total
Passivo Circulante
Passivo Circulante
Depósitos
Depósitos
Depósitos à Vista
Depósitos à Vista
Depósitos de Poupança
Depósitos de Poupança
Depósitos Interfinanceiros
Depósitos Interfinanceiros
Depósitos a Prazo
Depósitos a Prazo
Outros Depósitos
Outros Depósitos
Captações no Mercado Aberto
Captações no Mercado Aberto
Carteira Própria
Carteira Própria
Carteira de Terceiros
Carteira de Terceiros
Recursos de Aceites e Emissão de Títulos
Recursos de Aceites e Emissão de Títulos
Recursos Letras Imobiliárias, Hipotecárias, Créd. e Sim.
Recursos Letras Imobiliárias, Hipotecárias, Créd. e Sim.
Obrigações por TVM no Exterior
Obrigações por TVM no Exterior
Relações Interfinanceiras
Relações Interfinanceiras
Recebimentos e Pagamentos a Liquidar
Recebimentos e Pagamentos a Liquidar
Correspondentes
Correspondentes
Relações Interdependências
Relações Interdependências
Recursos em Trânsito de Terceiros
Recursos em Trânsito de Terceiros
Transferências Internas de Recursos
Transferências Internas de Recursos
Obrigações por Empréstimos
Obrigações por Empréstimos
Empréstimos no Exterior
Empréstimos no Exterior
Empréstimos no País - Instituições Oficiais
Empréstimos no País - Instituições Oficiais
Obrigações por Repasse do País
Obrigações por Repasse do País
Tesouro Nacional
Tesouro Nacional
BNDES
BNDES
Finame
Finame
Caixa Econômica Federal
Caixa Econômica Federal
Outras Instituições
Outras Instituições
Obrigações por Repasse do Exterior
Obrigações por Repasse do Exterior
Outras Obrigações
Outras Obrigações
Instrumentos Financeiros Derivativos
Instrumentos Financeiros Derivativos
Cobrança e Arrecadação de Tributos e Assemelhados
Cobrança e Arrecadação de Tributos e Assemelhados
Carteira de Câmbio
Carteira de Câmbio
Sociais e Estatutárias
Sociais e Estatutárias
Fiscais e Previdenciárias
Fiscais e Previdenciárias
Negociação e Intermediação de Valores
Negociação e Intermediação de Valores
Fundos Financeiros e de Desenvolvimento
Fundos Financeiros e de Desenvolvimento
Dívidas Subordinadas
Dívidas Subordinadas
Instrumentos Híbridos de Capital e Dívida
Instrumentos Híbridos de Capital e Dívida
Diversas
Diversas
Passivo Exigível a Longo Prazo
Passivo Exigível a Longo Prazo
Depósitos
Depósitos
Depósitos Interfinanceiros
Depósitos Interfinanceiros
Depósitos a Prazo
Depósitos a Prazo
Captações no Mercado Aberto
Captações no Mercado Aberto
Carteira Própria
Carteira Própria
Carteira de Terceiros
Carteira de Terceiros
Recursos de Aceites e Emissão de Títulos
Recursos de Aceites e Emissão de Títulos
Obrigações por TVM no Exterior
Obrigações por TVM no Exterior
Relações Interfinanceiras
Relações Interfinanceiras
Relações Interdependências
Relações Interdependências
Obrigações por Empréstimos
Obrigações por Empréstimos
Empréstimos no Exterior
Empréstimos no Exterior
Obrigações por Repasse do País
Obrigações por Repasse do País
Tesouro Nacional
Tesouro Nacional
BNDES
BNDES
Caixa Econômica Federal
Caixa Econômica Federal
Finame
Finame
Obrigações por Repasse do Exterior
Obrigações por Repasse do Exterior
Outras Obrigações
Outras Obrigações
Instrumentos Financeiros Derivativos
Instrumentos Financeiros Derivativos
Fiscais e Previdenciárias
Fiscais e Previdenciárias
Negociação e Intermediação de Valores
Negociação e Intermediação de Valores
Fundos Financeiros e de Desenvolvimento
Fundos Financeiros e de Desenvolvimento
Operações Especiais
Operações Especiais
Dívidas Subordinadas
Dívidas Subordinadas
Instrumentos Híbridos de Capital e Dívida
Instrumentos Híbridos de Capital e Dívida
Diversas
Diversas
Carteira de Câmbio
Carteira de Câmbio
Resultados de Exercícios Futuros
Resultados de Exercícios Futuros
Patrimônio Líquido
Patrimônio Líquido
Capital Social Realizado
Capital Social Realizado
De Domiciliados no País
De Domiciliados no País
De Domiciliados no Exterior
De Domiciliados no Exterior
Reservas de Capital
Reservas de Capital
Reservas de Reavaliação
Reservas de Reavaliação
Ativos Próprios
Ativos Próprios
Controladas/Coligadas e Equiparadas
Controladas/Coligadas e Equiparadas
Reservas de Lucro
Reservas de Lucro
Legal
Legal
Estatutária
Estatutária
Para Contingências
Para Contingências
De Lucros a Realizar
De Lucros a Realizar
Retenção de Lucros
Retenção de Lucros
Especial p/ Dividendos Não Distribuídos
Especial p/ Dividendos Não Distribuídos
Outras Reservas de Lucro
Outras Reservas de Lucro
Ações em Tesouraria
Ações em Tesouraria
Reservas para Expansão
Reservas para Expansão
Ajustes de Avaliação Patrimonial
Ajustes de Avaliação Patrimonial
Ajustes de Títulos e Valores Mobiliários
Ajustes de Títulos e Valores Mobiliários
Ajustes Acumulados de Conversão
Ajustes Acumulados de Conversão
Ajustes de Combinação de Negócios
Ajustes de Combinação de Negócios
Lucros/Prejuízos Acumulados
Lucros/Prejuízos Acumulados

"""
