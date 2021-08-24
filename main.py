from tkinter import *
from tkinter import messagebox
import pandas
from produto import Produto


BACKGROUND_COLOR = "#FFF6C4"
BACKGROUND_COLOR2 = "#E1FAFF"
BACKGROUND_COLOR3 = "#ABE2EE"
LETTER_COLOR = "#000187"
FONT = ("Arial", 14)
with open("locais_de_venda.txt") as file:
    LOCAIS_DE_VENDA = file.readlines()


####### ------------------------- CÁLCULO DA MARGEM DE LUCRO DE PRODUTO SINGULAR ------------------------- #######
def calcular(produto):
    global local

    custo = float(produto.cost)
    receita = float(produto.price)
    lucro = receita - custo
    valor_recebido = float(produto.v_received)
    margem_de_lucro = round((lucro/receita * 100), 2)
    taxa = round(((1 - (valor_recebido / receita)) * 100), 2)

    try:
        print(margem_de_lucro)
        print(local)
        print(taxa)
    except NameError:
        messagebox.showerror(title="Local inválido", message="Selecione o local de venda do produto.")
    else:
        messagebox.showinfo(title="Resultado", message=f"Sua margem de lucro nesse produto é de {margem_de_lucro}%.\n"
                                               f"A taxa cobrada por {local} foi de {taxa}%.")
        new_data = {"Produto": produto.code,
                    "Custo": custo,
                    "Vendido em": local,
                    "Vendido por": receita,
                    "Taxa cobrada": taxa,
                    "Margem de lucro": margem_de_lucro}

        if len(produto.code) == 0 or custo == 0 or receita == 0 or valor_recebido == 0:
            messagebox.showerror(title="Oops!", message="Não é possível salvar se houver campos vazios.")

        else:
            data = pandas.DataFrame([new_data])
            with open("infos_das_vendas.csv", 'a') as f:
                data.to_csv(f, header=False, index=False)
            entry_recebido.delete(0, END)
            entry_valor.delete(0, END)
            entry_custo.delete(0, END)
            entry_produto.delete(0, END)

####### ------------------------- CÁLCULO DA TAXA MÉDIA COBRADA POR DETERMINADO LOCAL DE VENDA ------------------------- #######
def get_tax():
    global local
    data = pandas.read_csv("infos_das_vendas.csv")

    try:
        print(local)
    except NameError:
        messagebox.showerror(title="Oops!", message='Você precisa selecionar o "local de venda" para calcular a taxa.')
    else:
        # Cria uma nova tabela [vendido em; taxa cobrada]
        nova_tabela = data.loc[:, ["Vendido em", "Taxa Cobrada"]]
        print(f"nova tabela: {nova_tabela}")
        # Reduz a tabela ao local selecionado
        pr_vendidos = nova_tabela[data["Vendido em"] == local]
        # Retorna a média dos valores da coluna "taxa cobrada" como float
        print(f"pr vendidos: {pr_vendidos}")

        taxa_data = float(pr_vendidos["Taxa Cobrada"].median(axis=0))
        taxa_data = round(taxa_data * 100, 2)

        return taxa_data


def tax_popup():
    try:
        print(local)
    except NameError:
        messagebox.showerror(title="Oops!", message='Você precisa selecionar o "local de venda" para calcular a taxa.')
    else:
        messagebox.showinfo(title=f"Taxa cobrada por {local}",
                        message=f'{local} cobra uma taxa média de {get_tax()}%.')

####### ------------------------- CÁLCULO DO VALOR MÍNIMO DE UM PRODUTO PARA LUCRO ------------------------- #######
def calc_min_valor():
    # Input do local
    global local
    try:
        print(local)
    except NameError:
        messagebox.showerror(title="Local inválido", message="Selecione o local de venda do produto.")
    else:
        taxa_do_local = get_tax()
        print(taxa_do_local)

        custo_do_produto = float(entry_custo.get().replace(",", "."))
        print(custo_do_produto)

        if custo_do_produto == "":
            messagebox.showerror(title="Valor inválido", message="Digite o custo do produto, usando somente números.")
        else:
            def abrir_tela_margem():
                new_window = Tk()
                new_window.config(padx=15, pady=15)
                new_window.title("Margem de lucro desejada")

                label = Label(new_window, text="Margem de lucro desejada, em %:")
                label.grid(column=1, row=1)

                global entry_margem
                entry_margem = Entry(new_window)
                entry_margem.grid(column=1, row=2)

                botao_add = Button(new_window, text="OK", command=store_margem, padx=10)
                botao_add.grid(column=1, row=3)

            def store_margem():
                try:
                    entrada = float(entry_margem.get())
                except ValueError:
                    messagebox.showerror(message="Valor inválido. Digite apenas usando números e ponto para as casas decimais.")
                else:
                    resultado = custo_do_produto * (entrada / 100 + 1) * (taxa_do_local / 100 + 1)
                    resultado = round(resultado, 2)
                    messagebox.showinfo(title="Resultado", message=f"Para ter lucro com esse produto, o valor final deverá ser de R${resultado}.\n"
                                             f"Custo: R${custo_do_produto}"
                                             f"\nMargem desejada: {entrada}%"
                                             f"\nTaxa cobrada por {local}: {taxa_do_local}%")


            abrir_tela_margem()
####### ------------------------- UI SETUP ------------------------- #######
window = Tk()
window.title("Gerenciador de Lucros")
window.config(bg=BACKGROUND_COLOR, padx=40, pady=30)

# Produto
label_produto = Label(window, text="Código do produto:")
label_produto.config(font=FONT, bg=BACKGROUND_COLOR, fg=LETTER_COLOR)
label_produto.grid(column=0, row=0)

entry_produto = Entry(window)
entry_produto.grid(column=1, row=0)

# Custo
label_custo = Label(window, text="  Custo: R$ ")
label_custo.config(font=FONT, bg=BACKGROUND_COLOR, fg=LETTER_COLOR)
label_custo.grid(column=2, row=0)

entry_custo = Entry(window)
entry_custo.grid(column=3, row=0)

# Local
label_local = Label(window, text="Colocado para venda em ")
label_local.config(font=FONT, bg=BACKGROUND_COLOR, fg=LETTER_COLOR)
label_local.grid(column=0, row=1)


def retorna_local(evt):
    global local
    local = local_listbox.get(evt.widget.curselection())


def populate_listbox():
    for i in LOCAIS_DE_VENDA:
        new_i = i.strip()
        local_listbox.insert(END, new_i)


local_listbox = Listbox(window, selectmode="SINGLE", height=5)
local_listbox.bind(sequence='<<ListboxSelect>>', func=retorna_local)
local_listbox.grid(column=1, row=1)
populate_listbox()


def abrir_tela_add():
    new_window = Tk()
    new_window.config(padx=15, pady=15)
    new_window.title("Adicionar local de venda")

    label = Label(new_window, text="Digite o nome do local de venda:")
    label.grid(column=1, row=1)

    global entry
    entry = Entry(new_window)
    entry.grid(column=1, row=2)

    botao_add = Button(new_window, text="Adicionar", command=add_local)
    botao_add.grid(column=1, row=3)

def add_local():
    with open("locais_de_venda.txt", "a") as file:
        file.write(f"\n{entry.get()}")
    local_listbox.insert(END, entry.get())
    messagebox.askokcancel(message="Feito!")


# Preço
label_valor = Label(window, text=" por R$ ")
label_valor.config(font=FONT, highlightthickness=0, bg=BACKGROUND_COLOR, fg=LETTER_COLOR)
label_valor.grid(column=2, row=1)

entry_valor = Entry(window)
entry_valor.grid(column=3, row=1)

# Valor recebido
label_recebido = Label(window, text=f"Valor recebido pela venda:")
label_recebido.config(font=FONT, highlightthickness=0, bg=BACKGROUND_COLOR, fg=LETTER_COLOR)
label_recebido.grid(column=0, row=2)

entry_recebido = Entry(window)
entry_recebido.grid(column=1, row=2)


def create_product():
    produto = Produto(entry_produto.get().replace(",", "."), entry_custo.get().replace(",", "."), entry_valor.get().replace(",", "."), entry_recebido.get().replace(",", "."))

    print(produto.code)
    print(produto.v_received)
    print(produto.cost)

    if len(produto.cost) == 0 or len(produto.v_received) == 0 or len(produto.price) == 0:
        messagebox.showerror(title="Oops!",
                            message="É preciso preencher todos os campos para prosseguir.")
    else:
        calcular(produto)

# Botão
botao = Button(window, text="Calcular margem de lucro e salvar", width=30, pady=10, command=create_product)
botao.grid(column=0, row=3, columnspan=2)

botao_taxa = Button(window, text="Verificar taxa média", width=30, pady=10, command=tax_popup)
botao_taxa.grid(column=0, row=4, columnspan=2)

botao_local_novo = Button(window, text="Adicionar local de venda", width=30, pady=10, command=abrir_tela_add)
botao_local_novo.grid(column=2, row=4, columnspan=2)

botao = Button(window, text="Calcular valor mínimo", width=30, pady=10, command=calc_min_valor)
botao.grid(column=2, row=3, columnspan=2)


window.mainloop()