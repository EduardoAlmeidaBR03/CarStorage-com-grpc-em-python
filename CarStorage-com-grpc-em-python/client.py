import tkinter as tk
from tkinter import messagebox
import grpc
import estoque_pb2
import estoque_pb2_grpc
from google.protobuf.empty_pb2 import Empty  # Importar a classe Empty corretamente

# Configuração do cliente gRPC
channel = grpc.insecure_channel("localhost:50051")
stub = estoque_pb2_grpc.EstoqueStub(channel)

# Funções da interface gráfica
def adicionar_carro():
    id_carro = id_entry.get()
    modelo_carro = modelo_entry.get()
    ano_carro = ano_entry.get()
    quantidade_carro = quantidade_entry.get()

    if not (id_carro and modelo_carro and ano_carro and quantidade_carro):
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    carro = estoque_pb2.Carro(
        id=id_carro,
        modelo=modelo_carro,
        ano=int(ano_carro),
        quantidade=int(quantidade_carro)
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
    carros = stub.ListarCarros(Empty())  # Uso corrigido da classe Empty
    lista.delete(0, tk.END)
    for carro in carros:
        lista.insert(tk.END, f"ID: {carro.id}, Modelo: {carro.modelo}, Ano: {carro.ano}, Quantidade: {carro.quantidade}")

# Interface gráfica
root = tk.Tk()
root.title("Estoque de Carros")

tk.Label(root, text="ID").grid(row=0, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)

tk.Label(root, text="Modelo").grid(row=1, column=0)
modelo_entry = tk.Entry(root)
modelo_entry.grid(row=1, column=1)

tk.Label(root, text="Ano").grid(row=2, column=0)
ano_entry = tk.Entry(root)
ano_entry.grid(row=2, column=1)

tk.Label(root, text="Quantidade").grid(row=3, column=0)
quantidade_entry = tk.Entry(root)
quantidade_entry.grid(row=3, column=1)

tk.Button(root, text="Adicionar Carro", command=adicionar_carro).grid(row=4, column=0)
tk.Button(root, text="Remover Carro", command=remover_carro).grid(row=4, column=1)
tk.Button(root, text="Listar Carros", command=listar_carros).grid(row=5, column=0, columnspan=2)

lista = tk.Listbox(root, width=50)
lista.grid(row=6, column=0, columnspan=2)

root.mainloop()
