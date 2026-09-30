import tkinter as tk
from tkinter import ttk, messagebox
import dados

def atualizar_tabela(filtro_texto="", filtro_situacao="Todos"):
    """Atualiza a tabela de exibição aplicando buscas e filtros."""
    for row in tree.get_children():
        tree.delete(row)

    lista = dados.carregar_dados()
    for aluno in lista:
        # Filtro por nome/série
        nome_match = filtro_texto.lower() in aluno['nome'].lower() or filtro_texto.lower() in aluno['serie'].lower()
        # Filtro por situação (Aprovado, Reprovado, Recuperação)
        situacao_match = (filtro_situacao == "Todos") or (aluno['situacao'] == filtro_situacao)

        if nome_match and situacao_match:
            tree.insert('', 'end', values=(
                aluno['id'], aluno['nome'], aluno['serie'], 
                f"{aluno['nota']:.1f}", aluno['situacao'], aluno['data_registro']
            ))
    atualizar_estatisticas()

def salvar():
    nome = entry_nome.get()
    serie = entry_serie.get()
    nota = entry_nota.get()

    sucesso, mensagem = dados.cadastrar_aluno(nome, serie, nota)
    if sucesso:
        messagebox.showinfo("Sucesso", mensagem)
        entry_nome.delete(0, tk.END)
        entry_serie.delete(0, tk.END)
        entry_nota.delete(0, tk.END)
        atualizar_tabela()
    else:
        messagebox.showerror("Erro de Validação", mensagem)

def deletar_selecionado():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Atenção", "Selecione um aluno na tabela para excluir!")
        return

    item_data = tree.item(selected_item[0])['values']
    aluno_id = item_data[0]

    if messagebox.askyesno("Confirmar", f"Deseja excluir o aluno ID {aluno_id}?"):
        dados.excluir_aluno(aluno_id)
        atualizar_tabela()

def atualizar_estatisticas():
    stats = dados.calcular_estatisticas()
    lbl_stats.config(
        text=f"Total: {stats['total']} | Média Geral: {stats['media']} | "
             f"Aprovados: {stats['aprovados']} | Rec: {stats['recuperacao']} | Reprovados: {stats['reprovados']}"
    )

# Configuração da janela Tkinter
app = tk.Tk()
app.title("Sistema de Notas de Alunos - Desktop")
app.geometry("750x550")

# Form de Cadastro
frame_form = tk.LabelFrame(app, text="Cadastrar Aluno", padx=10, pady=10)
frame_form.pack(fill="x", padx=10, pady=5)

tk.Label(frame_form, text="Nome:").grid(row=0, column=0)
entry_nome = tk.Entry(frame_form)
entry_nome.grid(row=0, column=1)

tk.Label(frame_form, text="Série:").grid(row=0, column=2)
entry_serie = tk.Entry(frame_form)
entry_serie.grid(row=0, column=3)

tk.Label(frame_form, text="Nota:").grid(row=0, column=4)
entry_nota = tk.Entry(frame_form)
entry_nota.grid(row=0, column=5)

btn_salvar = tk.Button(frame_form, text="Salvar Aluno", command=salvar, bg="green", fg="white")
btn_salvar.grid(row=0, column=6, padx=5)

# Barra de Pesquisa e Filtros
frame_busca = tk.Frame(app, padx=10, pady=5)
frame_busca.pack(fill="x")

tk.Label(frame_busca, text="Buscar:").pack(side="left")
entry_busca = tk.Entry(frame_busca)
entry_busca.pack(side="left", padx=5)

combo_filtro = ttk.Combobox(frame_busca, values=["Todos", "Aprovado", "Recuperação", "Reprovado"], state="readonly")
combo_filtro.set("Todos")
combo_filtro.pack(side="left", padx=5)

btn_filtrar = tk.Button(
    frame_busca, text="Filtrar", 
    command=lambda: atualizar_tabela(entry_busca.get(), combo_filtro.get())
)
btn_filtrar.pack(side="left")

btn_excluir = tk.Button(frame_busca, text="Excluir Selecionado", command=deletar_selecionado, bg="red", fg="white")
btn_excluir.pack(side="right")

# Tabela
cols = ("ID", "Nome", "Série", "Nota", "Situação", "Data/Hora")
tree = ttk.Treeview(app, columns=cols, show='headings')
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=110)
tree.pack(fill="both", expand=True, padx=10, pady=5)

# Label de Estatísticas
lbl_stats = tk.Label(app, text="", font=("Arial", 10, "bold"))
lbl_stats.pack(pady=5)

atualizar_tabela()
app.mainloop()