from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consultar_cnpj', methods=['POST'])
def consultar_cnpj():
    cnpj = request.form['cnpj']
    dados_empresa = consultar_dados_empresa(cnpj)
    return jsonify(dados_empresa)

def consultar_dados_empresa(cnpj):
    url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            nome_fantasia = data.get('fantasia', '')
            razao_social = data.get('nome', '')
            endereco = f"{data.get('logradouro', '')}, {data.get('numero', '')} - {data.get('bairro', '')}, {data.get('municipio', '')} - {data.get('uf', '')}"

            return {
                'nome_fantasia': nome_fantasia,
                'razao_social': razao_social,
                'endereco': endereco
            }
        else:
            return {'error': f"Erro na requisição: {data.get('message', 'Erro desconhecido')}"}
    except Exception as e:
        return {'error': f"Erro na requisição: {str(e)}"}

if __name__ == '__main__':
    app.run(debug=True)
