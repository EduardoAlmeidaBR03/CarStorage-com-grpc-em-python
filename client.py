import tkinter as tk
from tkinter import messagebox
import grpc
import estoque_pb2
import estoque_pb2_grpc
from google.protobuf.empty_pb2 import Empty

# Configuração do cliente gRPC
channel = grpc.insecure_channel("localhost:50051")
stub = estoque_pb2_grpc.EstoqueStub(channel)

# Funções da interface gráfica
def adicionar_carro():
    id_carro = id_entry.get()
    modelo_carro = modelo_entry.get()
    ano_carro = ano_entry.get()
    placa_carro = placa_entry.get()

    if not (id_carro and modelo_carro and ano_carro and placa_carro):
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    carro = estoque_pb2.Carro(
        id=id_carro,
        modelo=modelo_carro,
        ano=int(ano_carro),
        placa=placa_carro
    )
    resposta = stub.AdicionarCarro(carro)
    messagebox.showinfo("Resposta", resposta.status)

def remover_carro():
    id_carro = id_entry.get()
    if not id_carro:
        messagebox.showerror("Erro", "Preencha o ID do carro!")
        return

    request = estoque_pb2.RemoverRequest(id=id_carro)
    resposta = stub.RemoverCarro(request)
    messagebox.showinfo("Resposta", resposta.status)

def listar_carros():
    carros = stub.ListarCarros(Empty())
    lista.delete(0, tk.END)
    for carro in carros:
        lista.insert(tk.END, f"ID: {carro.id}, Modelo: {carro.modelo}, Ano: {carro.ano}, Placa: {carro.placa}")

# Interface gráfica
root = tk.Tk()
root.title("Estoque de Carros")

# --- Labels e Entries ---
tk.Label(root, text="ID").grid(row=0, column=0, sticky=tk.E)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Modelo").grid(row=1, column=0, sticky=tk.E)
modelo_entry = tk.Entry(root)
modelo_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Ano").grid(row=2, column=0, sticky=tk.E)
ano_entry = tk.Entry(root)
ano_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Placa").grid(row=3, column=0, sticky=tk.E)
placa_entry = tk.Entry(root)
placa_entry.grid(row=3, column=1, padx=5, pady=5)

# --- Botões ---
tk.Button(root, text="Adicionar Carro", command=adicionar_carro).grid(row=0, column=2, padx=5, pady=5, sticky=tk.N)
tk.Button(root, text="Remover Carro", command=remover_carro).grid(row=1, column=2, padx=5, pady=5)
tk.Button(root, text="Listar Carros", command=listar_carros).grid(row=2, column=2, padx=5, pady=5)

# --- Listbox ---
lista = tk.Listbox(root, width=100)
lista.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()