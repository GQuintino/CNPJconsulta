from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import requests
import csv
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://WEBSUP:ManutencaoWEBRemoto@127.0.0.1/dbCNPJ'
db = SQLAlchemy(app)

class cadcnpj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    nome_fantasia = db.Column(db.String(255))
    razao_social = db.Column(db.String(255))
    endereco = db.Column(db.String(255))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consultar_cnpj', methods=['POST'])
def consultar_cnpj():
    cnpj = request.form['cnpj']
    empresa = cadcnpj.query.filter_by(cnpj=cnpj).first()

    if empresa:
        dados_empresa = {
            'nome_fantasia': empresa.nome_fantasia,
            'razao_social': empresa.razao_social,
            'endereco': empresa.endereco
        }
    else:
        dados_empresa = consultar_dados_empresa(cnpj)
        if not dados_empresa.get('error'):
            nova_empresa = cadcnpj(
                cnpj=cnpj,
                nome_fantasia=dados_empresa['nome_fantasia'],
                razao_social=dados_empresa['razao_social'],
                endereco=dados_empresa['endereco']
            )
            db.session.add(nova_empresa)
            db.session.commit()

    return jsonify(dados_empresa)

@app.route('/exportar_csv', methods=['POST'])
def exportar_csv():
    cnpj = request.form['cnpj']
    empresa = cadcnpj.query.filter_by(cnpj=cnpj).first()

    if empresa:
        dados = [
            ['Nome Fantasia', 'Razão Social', 'Endereço'],
            [empresa.nome_fantasia, empresa.razao_social, empresa.endereco]
        ]

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(dados)

        output.seek(0)
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=empresa.csv"}
        )
    else:
        return jsonify({'error': 'Empresa não encontrada no banco de dados'})

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
