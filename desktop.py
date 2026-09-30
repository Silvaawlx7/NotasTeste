import tkinter as tk
from tkinter import ttk, messagebox
import dados

def atualizar_tabela(filtro_texto="", filtro_situacao="Todos"):
    """Atualiza a tabela de exibição aplicando buscas e filtros."""
    for row in tree.get_children():
        tree.delete(row)

    lista = dados.carregar_dados()
    for aluno in lista:
        nome_match = filtro_texto.lower() in aluno['nome'].lower() or filtro_texto.lower() in aluno['serie'].lower()
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

    if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o aluno ID {aluno_id}?"):
        dados.excluir_aluno(aluno_id)
        atualizar_tabela()

def atualizar_estatisticas():
    stats = dados.calcular_estatisticas()
    lbl_stats.config(
        text=f"Total: {stats['total']}   |   Média Geral: {stats['media']}   |   "
             f"Aprovados: {stats['aprovados']}   |   Recuperação: {stats['recuperacao']}   |   Reprovados: {stats['reprovados']}"
    )

# --- CONFIGURAÇÃO DA JANELA PRINCIPAL ---
app = tk.Tk()
app.title("Sistema de Gestão de Notas - Desktop")
app.geometry("820x620")
app.configure(bg="#f4f6f9")  # Fundo suave profissional

# Estilo TTK Moderno
style = ttk.Style()
style.theme_use("clam")

# Estilização da Tabela (Treeview)
style.configure("Treeview", 
    background="#ffffff", 
    foreground="#333333", 
    rowheight=30, 
    fieldbackground="#ffffff",
    font=("Segoe UI", 10)
)
style.configure("Treeview.Heading", 
    background="#2c3e50", 
    foreground="#ffffff", 
    font=("Segoe UI", 10, "bold")
)
style.map("Treeview", background=[('selected', '#3498db')])

# --- CABEÇALHO ---
frame_header = tk.Frame(app, bg="#2c3e50", height=60)
frame_header.pack(fill="x")

lbl_titulo = tk.Label(frame_header, text="🎓 Painel Acadêmico de Notas", font=("Segoe UI", 16, "bold"), bg="#2c3e50", fg="white")
lbl_titulo.pack(pady=12)

# --- CARD DE CADASTRO ---
frame_form = tk.LabelFrame(app, text=" Cadastrar Novo Aluno ", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#2c3e50", padx=15, pady=15, bd=1, relief="solid")
frame_form.pack(fill="x", padx=15, pady=12)

tk.Label(frame_form, text="Nome:", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#333").grid(row=0, column=0, sticky="w")
entry_nome = tk.Entry(frame_form, font=("Segoe UI", 10), width=18, bd=1, relief="solid")
entry_nome.grid(row=0, column=1, padx=(5, 15))

tk.Label(frame_form, text="Série:", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#333").grid(row=0, column=2, sticky="w")
entry_serie = tk.Entry(frame_form, font=("Segoe UI", 10), width=12, bd=1, relief="solid")
entry_serie.grid(row=0, column=3, padx=(5, 15))

tk.Label(frame_form, text="Nota:", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#333").grid(row=0, column=4, sticky="w")
entry_nota = tk.Entry(frame_form, font=("Segoe UI", 10), width=8, bd=1, relief="solid")
entry_nota.grid(row=0, column=5, padx=(5, 15))

btn_salvar = tk.Button(frame_form, text="➕ Salvar Aluno", command=salvar, bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", padx=10, pady=4)
btn_salvar.grid(row=0, column=6)

# --- BARRA DE PESQUISA E AÇÕES ---
frame_busca = tk.Frame(app, bg="#f4f6f9")
frame_busca.pack(fill="x", padx=15, pady=5)

tk.Label(frame_busca, text="🔍 Buscar:", font=("Segoe UI", 10, "bold"), bg="#f4f6f9", fg="#333").pack(side="left")
entry_busca = tk.Entry(frame_busca, font=("Segoe UI", 10), width=18, bd=1, relief="solid")
entry_busca.pack(side="left", padx=5)

combo_filtro = ttk.Combobox(frame_busca, values=["Todos", "Aprovado", "Recuperação", "Reprovado"], state="readonly", font=("Segoe UI", 10), width=12)
combo_filtro.set("Todos")
combo_filtro.pack(side="left", padx=5)

btn_filtrar = tk.Button(
    frame_busca, text="Filtrar", 
    command=lambda: atualizar_tabela(entry_busca.get(), combo_filtro.get()),
    bg="#2980b9", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", padx=8
)
btn_filtrar.pack(side="left")

btn_excluir = tk.Button(frame_busca, text="🗑️ Excluir Selecionado", command=deletar_selecionado, bg="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", padx=10, pady=4)
btn_excluir.pack(side="right")

# --- TABELA DE DADOS ---
frame_tabela = tk.Frame(app, bg="#ffffff")
frame_tabela.pack(fill="both", expand=True, padx=15, pady=10)

cols = ("ID", "Nome", "Série", "Nota", "Situação", "Data/Hora")
tree = ttk.Treeview(frame_tabela, columns=cols, show='headings')

tree.heading("ID", text="ID")
tree.column("ID", width=40, anchor="center")

tree.heading("Nome", text="Nome")
tree.column("Nome", width=180, anchor="w")

tree.heading("Série", text="Série")
tree.column("Série", width=100, anchor="center")

tree.heading("Nota", text="Nota")
tree.column("Nota", width=80, anchor="center")

tree.heading("Situação", text="Situação")
tree.column("Situação", width=120, anchor="center")

tree.heading("Data/Hora", text="Data/Hora Registro")
tree.column("Data/Hora", width=160, anchor="center")

tree.pack(fill="both", expand=True)

# --- RODAPÉ DE ESTATÍSTICAS ---
frame_stats = tk.Frame(app, bg="#ecf0f1", height=40, bd=1, relief="solid")
frame_stats.pack(fill="x", side="bottom")

lbl_stats = tk.Label(frame_stats, text="", font=("Segoe UI", 10, "bold"), bg="#ecf0f1", fg="#2c3e50")
lbl_stats.pack(pady=8)

atualizar_tabela()
app.mainloop()