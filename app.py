# ==============================================================================
# ARQUIVO: app.py
# OBJETIVO: Servidor web em Python que controla os dados e as funções do site.
# ==============================================================================

# Importamos do Flask apenas os 3 recursos que precisamos para a aula:
# 1. Flask: cria o servidor web.
# 2. render_template: junta os dados do Python com o arquivo visual index.html.
# 3. request: lê o que digitou na barra de pesquisa ou no formulário.
from flask import Flask, render_template, request

# Criamos a nossa aplicação web em Python
aplicacao = Flask(__name__)

# ==============================================================================
# 1. DADOS DO SITE (VARIÁVEIS E LISTAS DE DICIONÁRIOS)
# Funciona como um banco de dados simples na memória do computador.
# ==============================================================================

# Lista contendo 3 postagens. Cada postagem é um dicionário (chave: valor).
POSTAGENS = [
    {
        "titulo": "Primeiros Passos na Lógica com Python",
        "resumo": "Entenda como variáveis, listas e funções transformam ideias em programas reais.",
        "categoria": "Python",
        "autor": "Prof. de Tecnologia",
        "data": "10 Mai 2026",
        "imagem": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?auto=format&fit=crop&w=600&q=80"
    },
    {
        "titulo": "Criando Sites Responsivos com Bootstrap 5",
        "resumo": "Veja como o sistema de 12 colunas adapta a tela para celulares e computadores.",
        "categoria": "Web Design",
        "autor": "Ana Silva",
        "data": "12 Mai 2026",
        "imagem": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=600&q=80"
    },
    {
        "titulo": "A Diferença Entre HTML, CSS e Programação",
        "resumo": "Aprenda na prática o papel da estrutura, do estilo visual e da lógica no servidor.",
        "categoria": "Segurança",
        "autor": "Carlos Mendes",
        "data": "15 Mai 2026",
        "imagem": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=600&q=80"
    }
]

# Lista que guarda os comentários enviados
COMENTARIOS = [
    {
        "nome": "Maria Souza",
        "mensagem": "Muito fácil de entender a separação entre o HTML e o Python!"
    }
]


# ==============================================================================
# 2. FUNÇÕES DO SISTEMA (ONDE A LÓGICA DE PROGRAMAÇÃO ACONTECE)
# ==============================================================================

def filtrar_postagens(lista_completa, palavra_buscada, categoria_escolhida):
    """
    Função que recebe todas as postagens e devolve apenas as que combinam
    com a categoria clicada no menu e com a palavra digitada na busca.
    """
    # Criamos uma lista vazia para guardar apenas as postagens aprovadas no filtro
    resultado = []

    # Laço 'for': analisa uma postagem de cada vez dentro da lista completa
    for post in lista_completa:

        # 1º Teste: Verifica se a categoria é 'Todas' ou se é igual à categoria do post
        passou_na_categoria = (
            categoria_escolhida == "Todas" or
            post["categoria"].lower() == categoria_escolhida.lower()
        )

        # 2º Teste: Verifica se a palavra buscada aparece no título ou no resumo
        texto_do_post = (post["titulo"] + " " + post["resumo"]).lower()
        passou_na_busca = palavra_buscada.lower() in texto_do_post

        # Condicional 'if': Se passou nos dois testes, adiciona na lista de resultado
        if passou_na_categoria and passou_na_busca:
            resultado.append(post)

    # Retorna a lista final já filtrada
    return resultado


# ==============================================================================
# 3. ROTAS DA APLICAÇÃO (CONECTAM OS ENDEREÇOS DO NAVEGADOR AO PYTHON)
# ==============================================================================

@aplicacao.route("/", methods=["GET"])
def pagina_inicial():
    """
    Rota Principal ('/'): É executada sempre que alguém abre o site,
    clica em uma categoria do menu ou faz uma pesquisa.
    """
    # Lê o que veio na URL (ex: ?busca=python&categoria=Iniciantes)
    # Se o usuário não digitou nada, assume "" para busca e "Todas" para categoria
    termo_busca = request.args.get("busca", "").strip()
    categoria_atual = request.args.get("categoria", "Todas").strip()

    # Chama a nossa função lógica para filtrar os artigos
    postagens_visiveis = filtrar_postagens(POSTAGENS, termo_busca, categoria_atual)

    # Entrega o arquivo 'index.html' preenchido com as variáveis do Python
    return render_template(
        "index.html",
        postagens=postagens_visiveis,
        comentarios=COMENTARIOS,
        termo_busca=termo_busca,
        categoria_atual=categoria_atual,
        aviso_sucesso=None,
        erro_404=False
    )


@aplicacao.route("/comentar", methods=["POST"])
def adicionar_comentario():
    """
    Rota de Comentários ('/comentar'): É executada quando o aluno preenche
    o formulário no final da página e clica em 'Publicar Comentário'.
    """
    # Captura o nome e a mensagem digitados nos campos do formulário HTML
    nome_aluno = request.form.get("nome", "").strip()
    texto_mensagem = request.form.get("mensagem", "").strip()

    # Condicional 'if': Só salva se o aluno preencheu os dois campos
    if nome_aluno and texto_mensagem:
        novo_item = {
            "nome": nome_aluno,
            "mensagem": texto_mensagem
        }
        # Insere o comentário na posição 0 (no topo da lista de comentários)
        COMENTARIOS.insert(0, novo_item)
        mensagem_retorno = f"Comentário de {nome_aluno} salvo pelo Python com sucesso!"
    else:
        mensagem_retorno = "Preencha seu nome e sua mensagem para publicar."

    # Recarrega a página mostrando o novo comentário e o aviso de confirmação
    return render_template(
        "index.html",
        postagens=POSTAGENS,
        comentarios=COMENTARIOS,
        termo_busca="",
        categoria_atual="Todas",
        aviso_sucesso=mensagem_retorno,
        erro_404=False
    )


@aplicacao.errorhandler(404)
def pagina_nao_encontrada(erro):
    """
    Rota de Erro 404: É acionada automaticamente quando o usuário digita
    um endereço que não existe no site (ex: localhost:5000/nao-existe).
    """
    return render_template(
        "index.html",
        postagens=POSTAGENS,
        comentarios=COMENTARIOS,
        termo_busca="",
        categoria_atual="Todas",
        aviso_sucesso=None,
        erro_404=True
    ), 404


# ==============================================================================
# 4. COMANDO QUE LIGA O SERVIDOR
# ==============================================================================
if __name__ == "__main__":
    # Inicia o servidor na porta 5000 com 'debug=True' (atualiza ao salvar alterações)
    aplicacao.run(debug=True, port=5000)