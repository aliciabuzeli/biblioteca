from flask import Flask, request, redirect, render_template, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'minha_chave'

livros = []


def obter_livro(codigo):
    if 0 <= codigo < len(livros):
        return livros[codigo]
    return None


@app.route('/')
def index():
    return render_template('index.html', livros=livros)


@app.route('/adicionar_livro', methods=['GET', 'POST'])
def adicionar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        codigo = len(livros)
        livro = {
            "codigo": codigo,
            "titulo": titulo,
            "autor": autor,
            "ano": datetime.now().year,
            "devolver_ate": None
        }
        livros.append(livro)
        flash('Livro adicionado com sucesso!')
        return redirect('/')
    return render_template('adicionar_livro.html')


@app.route('/emprestar_livro/<int:codigo>')
def emprestar_livro(codigo):
    livro = obter_livro(codigo)
    if livro:
        if not livro["devolver_ate"]:
            data_devolucao = datetime.now() + timedelta(days=7)
            livro["devolver_ate"] = data_devolucao
            flash(f"Livro emprestado! Devolver até {data_devolucao.strftime('%d/%m/%Y')}.")
        else:
            flash("Este livro já está emprestado.")
    else:
        flash("Livro não encontrado.")
    return redirect('/')


@app.route('/devolver_livro/<int:codigo>')
def devolver_livro(codigo):
    livro = obter_livro(codigo)
    if livro:
        if livro["devolver_ate"]:
            hoje = datetime.now()
            atraso = (hoje - livro["devolver_ate"]).days
            if atraso > 0:
                multa = 10 + atraso
                flash(f'Livro devolvido com {atraso} dias de atraso. Multa: R${multa}')
            else:
                flash('Livro devolvido no prazo.')
            livro["devolver_ate"] = None
        else:
            flash('Este livro não está emprestado.')
    else:
        flash("Livro não encontrado.")
    return redirect('/')


@app.route('/editar_livro/<int:codigo>', methods=['GET', 'POST'])
def editar_livro(codigo):
    livro = obter_livro(codigo)
    if not livro:
        flash("Livro não encontrado.")
        return redirect('/')

    if request.method == 'POST':
        livro["titulo"] = request.form['titulo']
        livro["autor"] = request.form['autor']
        flash('Livro atualizado com sucesso!')
        return redirect('/')

    return render_template('editar_livro.html', livro=livro)


@app.route('/apagar_livro/<int:codigo>')
def apagar_livro(codigo):
    if 0 <= codigo < len(livros):
        del livros[codigo]
        for i, livro in enumerate(livros):
            livro["codigo"] = i
        flash('Livro excluído com sucesso!')
    else:
        flash("Livro não encontrado.")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
