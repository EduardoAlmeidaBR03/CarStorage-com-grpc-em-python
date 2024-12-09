import grpc
from concurrent import futures
from google.protobuf import empty_pb2
import estoque_pb2
import estoque_pb2_grpc

# Classe do serviço gRPC
class EstoqueServicer(estoque_pb2_grpc.EstoqueServicer):
    def __init__(self):
        self.estoque = []

    def AdicionarCarro(self, request, context):
        carro = {
            "id": request.id,
            "modelo": request.modelo,
            "ano": request.ano,
            "quantidade": request.quantidade
        }
        self.estoque.append(carro)
        return estoque_pb2.Resposta(status="Carro adicionado com sucesso!")

    def RemoverCarro(self, request, context):
        self.estoque = [carro for carro in self.estoque if carro["id"] != request.id]
        return estoque_pb2.Resposta(status="Carro removido com sucesso!")

    def ListarCarros(self, request, context):
        for carro in self.estoque:
            yield estoque_pb2.Carro(
                id=carro["id"],
                modelo=carro["modelo"],
                ano=carro["ano"],
                quantidade=carro["quantidade"]
            )

# Inicialização do servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    estoque_pb2_grpc.add_EstoqueServicer_to_server(EstoqueServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("Servidor gRPC rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
