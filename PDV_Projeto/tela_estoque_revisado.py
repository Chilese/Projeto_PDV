import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

combo_categoria_id = None
combo_fornecedor = None

# Variável global para armazenar a árvore (Treeview)
tree = None

def obter_nomes_fornecedores():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT nome_fantasia FROM fornecedor''')
    fornecedores = cursor.fetchall()
    conn.close()
    return [fornecedor[0] for fornecedor in fornecedores]

def obter_nomes_categorias():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT categoria FROM categoria''')
    categorias = cursor.fetchall()
    conn.close()
    return [categoria[0] for categoria in categorias]

# Função para buscar todos os produtos do banco de dados
def buscar_produtos():
    # Conecta ao banco de dados e busca todos os produtos na tabela "estoque"
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM estoque''')
    produtos = cursor.fetchall()
    conn.close()
    return produtos

# Função para abrir a janela de cadastro de produtos (interface.py)
def abrir_interface_cadastro():
    import cadastro_produto

# Função para abrir a janela de edição do produto
def editar_produto(event):
    # Obtenha o item selecionado na árvore
    item_id = tree.selection()[0]
    
    # Obtenha os valores atuais do produto com base no item_id
    valores = tree.item(item_id, 'values')

    def salvar_edicoes():
        print("Função salvar_edicoes chamada")  # Adicione esta linha
        item_id = tree.selection()[0]  # Obtenha o item selecionado na árvore
        produto_id = tree.item(item_id, 'values')[0]  # Obtenha o ID do produto


        novo_nome = entry_nome.get()
        nova_descricao = entry_descricao.get()
        nova_categoria = combo_categoria_id.get()
        novo_preco_compra = entry_preco_compra.get()
        novo_preco_venda = entry_preco_venda.get()
        nova_quantidade = entry_quantidade.get()
        nova_data_entrada = entry_data_entrada.get()
        novo_fornecedor = combo_fornecedor.get()
        novas_notas = entry_notas.get()


        # Atualize os detalhes do produto no banco de dados com base no item_id
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()

        print("Valores dos Campos de Entrada:")
        print("Nome:", novo_nome)
        print("Descrição:", nova_descricao)
        print("Categoria:", nova_categoria)
        print("Preço de Compra:", novo_preco_compra)    
        print("Preço de Venda:", novo_preco_venda)
        print("Quantidade:", nova_quantidade)
        print("Data de Entrada:", nova_data_entrada)
        print("Fornecedor:", novo_fornecedor)
        print("Notas:", novas_notas)

        try:
            cursor.execute('''UPDATE estoque SET nome = ?, descricao = ?, categoria_id = ?, preco_compra = ?, preco_venda = ?, quantidade = ?, data_entrada = ?, fornecedor_id = ?, notas = ? WHERE id = ?''', (novo_nome, nova_descricao, nova_categoria, novo_preco_compra, novo_preco_venda, nova_quantidade, nova_data_entrada, novo_fornecedor, novas_notas, produto_id))
            conn.commit()
            conn.close()
            print("Atualização bem-sucedida")

            # Atualize a exibição na árvore (Treeview)
            tree.item(item_id, values=(valores[0], novo_nome, nova_descricao, nova_categoria, novo_preco_compra, novo_preco_venda, nova_quantidade, nova_data_entrada, novo_fornecedor, novas_notas))
            
            # Feche a janela de edição após salvar
            popup.destroy()
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            messagebox.showerror('Erro', f'Erro ao atualizar o produto: {e}')
            print(f"Erro ao atualizar o produto: {e}")

    
    # Crie uma janela pop-up para edição
    popup = tk.Toplevel(root)
    popup.title('Editar Produto')

  
    # Preencha esses campos com os valores atuais

    # Nome
    label_nome = tk.Label(popup, text='Nome:')
    label_nome.pack()
    entry_nome = tk.Entry(popup)
    entry_nome.insert(0, valores[1])  # Insira o valor atual
    entry_nome.pack()

    # Descrição
    label_descricao = tk.Label(popup, text='Descrição:')
    label_descricao.pack()
    entry_descricao = tk.Entry(popup)
    entry_descricao.insert(0, valores[2])  # Insira o valor atual
    entry_descricao.pack()

    # Categoria
    label_categoria = tk.Label(popup, text='Categoria:')
    label_categoria.pack()
    combo_categoria_id = ttk.Combobox(popup, values=obter_nomes_categorias())  # Configuração do combobox
    combo_categoria_id.set(valores[3])  # Defina o valor atual
    combo_categoria_id.pack()

    # Preço de Compra (você pode adicionar campos semelhantes para outros atributos)
    label_preco_compra = tk.Label(popup, text='Preço de Compra:')
    label_preco_compra.pack()
    entry_preco_compra = tk.Entry(popup)
    entry_preco_compra.insert(0, valores[4])  # Insira o valor atual
    entry_preco_compra.pack()

    # Preço de Venda (você pode adicionar campos semelhantes para outros atributos)
    label_preco_venda = tk.Label(popup, text='Preço de Venda:')
    label_preco_venda.pack()
    entry_preco_venda = tk.Entry(popup)
    entry_preco_venda.insert(0, valores[5])  # Insira o valor atual
    entry_preco_venda.pack()

    # Quantidade (você pode adicionar campos semelhantes para outros atributos)
    label_quantidade = tk.Label(popup, text='Quantidade:')
    label_quantidade.pack()
    entry_quantidade = tk.Entry(popup)
    entry_quantidade.insert(0, valores[6])  # Insira o valor atual
    entry_quantidade.pack()

    # Data de Entrada
    label_data_entrada = tk.Label(popup, text='Data de Entrada:')
    label_data_entrada.pack()
    entry_data_entrada = tk.Entry(popup)
    entry_data_entrada.insert(0, valores[7])
    entry_data_entrada.pack()

    # Fornecedor
    label_fornecedor = tk.Label(popup, text='Fornecedor:')
    label_fornecedor.pack()
    combo_fornecedor = ttk.Combobox(popup, values=obter_nomes_fornecedores())  # Configuração da combobox
    combo_fornecedor.set(valores[8])  # Defina o valor atual
    combo_fornecedor.pack()

    # Notas
    label_notas = tk.Label(popup, text='Notas:')
    label_notas.pack()
    entry_notas = tk.Entry(popup)
    entry_notas.insert(0, valores[9])
    entry_notas.pack()

    # Botão para salvar as edições
    btn_salvar = tk.Button(popup, text='Salvar Edições', command=salvar_edicoes)
    btn_salvar.pack()

# Função para excluir o produto
def excluir_produto():
    # Obtenha o ID do produto selecionado na árvore
    item_id = tree.selection()[0]

    if item_id:
        # Exibir uma mensagem de confirmação antes da exclusão
        resultado = messagebox.askquestion('Excluir Produto', 'Você tem certeza que deseja excluir este produto?')

        if resultado == 'yes':
            try:
                # Conectar ao banco de dados
                conn = sqlite3.connect('estoque.db')
                cursor = conn.cursor()

                # Obtenha o ID do produto a ser excluído
                produto_id = int(tree.item(item_id, 'values')[0])

                # Executar a consulta SQL DELETE para remover o produto
                cursor.execute('''DELETE FROM estoque WHERE id = ?''', (produto_id,))

                # Confirmar a transação
                conn.commit()

                # Fechar a conexão com o banco de dados
                conn.close()

                # Remover o produto da árvore
                tree.delete(item_id)
            except sqlite3.Error as e:
                messagebox.showerror('Erro', f'Erro ao excluir o produto: {e}')

# Cria a janela da interface de listagem de produtos
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Lista de Produtos')

    tree = ttk.Treeview(root, columns=("ID", "Nome", "Descrição", "Categoria", "Preço de Compra", "Preço de Venda", "Quantidade", "Data de Entrada", "Fornecedor", "Notas"), show="headings")

    # Definindo os cabeçalhos das colunas
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Categoria", text="Categoria")
    tree.heading("Preço de Compra", text="Preço de Compra")
    tree.heading("Preço de Venda", text="Preço de Venda")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Data de Entrada", text="Data de Entrada")
    tree.heading("Fornecedor", text="Fornecedor")
    tree.heading("Notas", text="Notas")

    # Definindo o tamanho máximo de cada coluna
    tree.column("ID", width=50)
    tree.column("Nome", width=150)
    tree.column("Descrição", width=200)
    tree.column("Categoria", width=100)
    tree.column("Preço de Compra", width=100)
    tree.column("Preço de Venda", width=100)
    tree.column("Quantidade", width=80)
    tree.column("Data de Entrada", width=100)
    tree.column("Fornecedor", width=150)
    tree.column("Notas", width=200)

    tree.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # Busca os produtos no banco de dados
    produtos = buscar_produtos()

    # Insere os produtos na tabela (Treeview)
    for produto in produtos:
        tree.insert("", tk.END, values=produto)

    # Configura a função para lidar com a abertura da janela de edição
    tree.bind("<Double-1>", editar_produto)

    # Botão para excluir o produto
    btn_excluir = tk.Button(root, text="Excluir Produto", command=excluir_produto)
    btn_excluir.grid(row=1, column=0, padx=10, pady=10)

    root.mainloop()