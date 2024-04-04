import requests

def consultar_dados_empresa(cnpj):
    url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
    try:
        response = requests.get(url)
        data = response.json()

        # Verificando se a requisição foi bem-sucedida
        if response.status_code == 200:
            nome_fantasia = data['fantasia']
            razao_social = data['nome']
            endereco = f"{data['logradouro']}, {data['numero']} - {data['bairro']}, {data['municipio']} - {data['uf']}"
            
            return {
                'nome_fantasia': nome_fantasia,
                'razao_social': razao_social,
                'endereco': endereco
            }
        else:
            return {'error': f"Erro na requisição: {data['message']}"}
    except Exception as e:
        return {'error': f"Erro na requisição: {str(e)}"}

# Exemplo de uso
cnpj = 'seu_cnpj_aqui'
dados_empresa = consultar_dados_empresa(cnpj)

if 'error' in dados_empresa:
    print(f"Erro: {dados_empresa['error']}")
else:
    print(f"Nome Fantasia: {dados_empresa['nome_fantasia']}")
    print(f"Razão Social: {dados_empresa['razao_social']}")
    print(f"Endereço: {dados_empresa['endereco']}")
    