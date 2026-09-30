from flask import Flask, render_template, request, redirect, url_for, flash
import dados

app = Flask(__name__)
app.secret_key = "chave_secreta_projeto"

@app.route('/')
def index():
    # Obtém parâmetros de pesquisa/filtro da URL
    busca = request.args.get('busca', '')
    filtro_situacao = request.args.get('situacao', 'Todos')

    todos_alunos = dados.carregar_dados()
    alunos_filtrados = []

    for a in todos_alunos:
        match_busca = busca.lower() in a['nome'].lower() or busca.lower() in a['serie'].lower()
        match_situacao = (filtro_situacao == 'Todos') or (a['situacao'] == filtro_situacao)
        if match_busca and match_situacao:
            alunos_filtrados.append(a)

    stats = dados.calcular_estatisticas()
    return render_template('index.html', alunos=alunos_filtrados, stats=stats, busca=busca, situacao_selecionada=filtro_situacao)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    serie = request.form.get('serie')
    nota = request.form.get('nota')

    sucesso, msg = dados.cadastrar_aluno(nome, serie, nota)
    flash(msg, 'success' if sucesso else 'danger')
    return redirect(url_for('index'))

@app.route('/excluir/<int:aluno_id>')
def excluir(aluno_id):
    sucesso, msg = dados.excluir_aluno(aluno_id)
    flash(msg, 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)