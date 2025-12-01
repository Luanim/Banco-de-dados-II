import psycopg2
import xml.etree.ElementTree as ET

def conectar_postgres():
    try:
        conexao = psycopg2.connect(
            host="localhost",
            database="banco",
            user="postgres",
            password="postgres"
        )
        return conexao
    except Exception as e:
        print("Erro ao conectar ao PostgreSQL:", e)
        return None

def buscar_dados_peca(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Peca;")
        linhas = cursor.fetchall()
        cursor.close()
        return linhas
    except Exception as e:
        print("Erro ao buscar dados da tabela Peca:", e)
        return []

def analisar_xml_fornecimento(caminho_arquivo):
    try:
        arvore = ET.parse(caminho_arquivo)
        raiz = arvore.getroot()
        dados_fornecimento = []
        for linha in raiz.findall('row'):
            dados_fornecimento.append({
                'codigo': linha.find('codigo').text,
                'cod_fornec': linha.find('cod_fornec').text,
                'cod_peca': linha.find('cod_peca').text,
                'cod_proj': linha.find('cod_proj').text,
                'quantidade': linha.find('quantidade').text,
                'valor': linha.find('valor').text
            })
        return dados_fornecimento
    except Exception as e:
        print("Erro ao analisar o arquivo XML:", e)
        return []

def juntar_dados(dados_peca, dados_fornecimento):
    dados_juntos = []
    for fornecimento in dados_fornecimento:
        for peca in dados_peca:
            if int(fornecimento['cod_peca']) == peca[0]:  # Comparar cod_peca
                dados_juntos.append({
                    'codigo': fornecimento['codigo'],
                    'nome_peca': peca[1],
                    'cor_peca': peca[2],
                    'quantidade': fornecimento['quantidade'],
                    'valor': fornecimento['valor']
                })
    return dados_juntos

def principal():
    # Conectar ao PostgreSQL
    conexao = conectar_postgres()
    if not conexao:
        return

    # Buscar dados da tabela Peca
    dados_peca = buscar_dados_peca(conexao)

    # Analisar Fornecimento.xml
    dados_fornecimento = analisar_xml_fornecimento("Fornecimento.xml")

    # Juntar dados
    dados_juntos = juntar_dados(dados_peca, dados_fornecimento)

    # Exibir dados unidos
    print("Dados Unidos:")
    for dado in dados_juntos:
        print(dado)

    # Fechar a conexão com o banco de dados
    conexao.close()

if __name__ == "__main__":
    principal()