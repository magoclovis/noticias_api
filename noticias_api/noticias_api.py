from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NEWS_API_KEY = "936db3e2de1c489aab5bd5c79abf7fe5"

noticias = {
    "Tecnologia": {
        "Celulares": [],
        "Computadores": [],
        "Programação": []
    },
    "Jogos": {
        "Luta": [],
        "Celulares": [],
        "Consoles": [],
        "Terror": [],
        "Computadores": [],
        "Campeonatos": {
            "Passados": [],
            "Futuros": []
        }
    }
}

categorias_disponiveis = list(noticias.keys())

# listar as categorias que foram adicionas
@app.route('/categorias', methods=['GET'])
def obter_categorias():
    return jsonify({"categorias": categorias_disponiveis})

# apresentar a noticia (título e conteúdo)
@app.route('/noticias', methods=['GET'])
def obter_noticias():
    try:
        categoria = request.args.get('categoria')
        subcategoria = request.args.get('subcategoria')
        palavra_chave = request.args.get('palavra_chave')

        if categoria not in noticias:
            return jsonify({"mensagem": f"Nenhuma notícia na categoria '{categoria}'"}), 404

        if subcategoria and subcategoria not in noticias[categoria]:
            return jsonify({"mensagem": f"Nenhuma notícia na subcategoria '{subcategoria}'"}), 404

        if subcategoria:
            noticias_filtradas = [noticia for noticia in noticias[categoria][subcategoria]]
        else:
            noticias_filtradas = [noticia for subcat in noticias[categoria].values() for noticia in subcat]

        if palavra_chave:
            noticias_filtradas = [noticia for noticia in noticias_filtradas if palavra_chave.lower() in noticia['titulo'].lower()]

        return jsonify(noticias_filtradas)
    except Exception as e:
        return jsonify({"mensagem": str(e)}), 500

# adicionar as noticias
@app.route('/noticias/adicionar', methods=['POST'])
def adicionar_noticia():
    try:
        data = request.get_json()
        if not data or "categoria" not in data or "subcategoria" not in data or "titulo" not in data or "conteudo" not in data:
            return jsonify({"mensagem": "Dados inválidos"}), 400

        categoria = data["categoria"]
        subcategoria = data["subcategoria"]
        if categoria not in noticias:
            noticias[categoria] = {}
        if subcategoria not in noticias[categoria]:
            noticias[categoria][subcategoria] = []

        nova_noticia = {
            "id": len(noticias[categoria][subcategoria]) + 1,
            "titulo": data["titulo"],
            "conteudo": data["conteudo"]
        }
        noticias[categoria][subcategoria].append(nova_noticia)
        return jsonify({"mensagem": "Notícia adicionada com sucesso!"})
    except Exception as e:
        return jsonify({"mensagem": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
