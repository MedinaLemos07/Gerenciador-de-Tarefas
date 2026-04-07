# Essa camada é responsável por tudo que envolve salvar e carregar dados.
# Separei aqui para que o gerenciador.py não precise saber como os dados
# são armazenados — ele só chama as funções e recebe o resultado.

import json

from models.tarefa import Tarefa  # Preciso da classe Tarefa para recriar os objetos ao carregar


def salvar_tarefas(tarefas):
    # Abre o arquivo para escrita ("w"). Se ele não existir, o Python cria.
    # Se já existir, o conteúdo anterior é substituído — isso é intencional,
    # porque sempre salvo a lista completa e atualizada.
    with open("tarefas.json", "w", encoding="utf-8") as arquivo:

        # Converto cada objeto Tarefa em dicionário antes de salvar,
        # porque o json.dump não sabe como serializar objetos customizados.
        # O indent=4 deixa o JSON indentado e legível se eu abrir o arquivo.
        # O ensure_ascii=False garante que acentos (é, ã, ç) sejam salvos
        # como texto normal, e não como códigos como \u00e9.
        json.dump(
            [tarefa.to_dict() for tarefa in tarefas],
            arquivo,
            indent=4,
            ensure_ascii=False,
        )


def carregar_tarefas():
    try:
        # Abre o arquivo para leitura ("r").
        with open("tarefas.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)  # Lê o JSON e transforma em lista de dicionários

            # Converto cada dicionário de volta para um objeto Tarefa
            # usando o método estático que criei na classe.
            return [Tarefa.from_dict(dado) for dado in dados]

    except FileNotFoundError:
        # Se o arquivo ainda não existe (primeira vez rodando o programa),
        # simplesmente começo com uma lista vazia em vez de travar com erro.
        return []

    except json.JSONDecodeError:
        # Se o arquivo existe mas está corrompido (ex: foi editado manualmente
        # e ficou com o formato errado), aviso o usuário e começo do zero.
        print("Aviso: arquivo de tarefas corrompido. Iniciando com lista vazia.")
        return []
    
        #LUAN MEDINA - 2024-06-17