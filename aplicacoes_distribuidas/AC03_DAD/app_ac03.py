from flask import Flask 
from flask import request 
from flask import jsonify
from flask import render_template
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

app_ac03 = Flask(__name__)
app_ac03.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbimpacta:impacta#2020@dbimpacta.postgresql.dbaas.com.br/dbimpacta'
db = SQLAlchemy(app_ac03)


class MaapSystem(db.Model):
    ra = db.Column(db.Integer, primary_key = True)
    nome_do_aluno = db.Column(db.String(50), nullable=True)
    email_do_aluno = db.Column(db.String(50), nullable=True)
    logradouro = db.Column(db.String(50), nullable=True)
    numero = db.Column(db.String(5), nullable=True)
    cep = db.Column(db.String(10), nullable=True)
    complemento = db.Column(db.String(20), nullable=True)

    def __init__(self, ra, nome_do_aluno, email_do_aluno, logradouro, numero, cep, complemento):
        self.ra = ra
        self.nome_do_aluno = nome_do_aluno
        self.email_do_aluno = email_do_aluno
        self.logradouro = logradouro
        self.numero = numero
        self.cep = cep
        self.complemento = complemento


@app_ac03.route("/")
@app_ac03.route("/index")
def index():
    resposta = MaapSystem.query.all()
    return render_template("index.html", resposta=resposta)


@app_ac03.route("/add", methods=['GET','POST'])
def add():
    if request.method == 'POST':
        aluno = MaapSystem(request.form['ra'], request.form['nome'], request.form['email'], request.form['logradouro'], request.form['numero'] , request.form['cep'], request.form['complemento'])
        db.session.add(aluno)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app_ac03.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    aluno = MaapSystem.query.get(id)
    if request.method == 'POST':
        aluno.ra = request.form['ra']
        aluno.nome_do_aluno = request.form['nome']
        aluno.email_do_aluno = request.form['email']
        aluno.logradouro = request.form['logradouro']
        aluno.numero = request.form['numero']
        aluno.cep = request.form['cep']
        aluno.complemento = request.form['complemento']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', aluno=aluno)


@app_ac03.route("/delete/<int:id>")
def delete(id):
    aluno = MaapSystem.query.get(id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app_ac03.run(debug=True)

'''
select * from maap_system
delete from maap_system
'''