import tkinter as tk
from tkinter import messagebox
import requests

# menu onde seria listado as categorias buscadas pela API e o usuário (através do menu suspenso) escolheria qual categoria quer ler sobre

class categoria_noticias:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicação de Notícias")

        self.categorias = self.obter_categorias()

        self.categoria_var = tk.StringVar()
        self.categoria_var.set(self.categorias[0])

        self.label = tk.Label(root, text="Selecione uma categoria:")
        self.label.pack()

        self.categoria_menu = tk.OptionMenu(root, self.categoria_var, *self.categorias)
        self.categoria_menu.pack()

        self.mostrar_noticias_button = tk.Button(root, text="Mostrar Notícias", command=self.mostrar_noticias)
        self.mostrar_noticias_button.pack()

    def obter_categorias(self):
        response = requests.get("http://127.0.0.1:5000/categorias")
        data = response.json()
        return data["categorias"]

    def mostrar_noticias(self):
        categoria = self.categoria_var.get()
        if categoria:
            self.mostrar_noticias_por_categoria(categoria)
        else:
            messagebox.showwarning("Erro", "Selecione uma categoria antes de mostrar as notícias.")

    def mostrar_noticias_por_categoria(self, categoria):
        response = requests.get(f"http://127.0.0.1:5000/noticias?categoria={categoria}")
        data = response.json()

        noticias_text = "\n\n".join([f"Título: {noticia['titulo']}\nConteúdo: {noticia['conteudo']}" for noticia in data])
        messagebox.showinfo(f"Notícias - Categoria: {categoria}", noticias_text)

if __name__ == '__main__':
    root = tk.Tk()
    app = categoria_noticias(root)
    root.mainloop()
