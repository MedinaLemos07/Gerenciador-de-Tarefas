# Aqui fica o "molde" de uma tarefa. Sempre que eu criar uma tarefa nova,
# ela vai seguir exatamente esse formato: descrição, prioridade e se está concluída.


class Tarefa:
    # Esse método roda automaticamente quando eu crio uma tarefa nova.
    # Os valores padrão garantem que, se eu não informar prioridade ou status,
    # a tarefa já nasce com "baixa" e "não concluída".
    def __init__(self, descricao, prioridade="baixa", concluida=False):
        self.descricao = descricao
        self.prioridade = prioridade
        self.concluida = concluida

    # Converte a tarefa para um dicionário Python.
    # Preciso disso porque o JSON não entende objetos — só entende texto,
    # números, listas e dicionários. Então antes de salvar, converto.
    def to_dict(self):
        return {
            "descricao": self.descricao,
            "prioridade": self.prioridade,
            "concluida": self.concluida,
        }

    # Faz o caminho inverso: recebe um dicionário vindo do JSON
    # e monta um objeto Tarefa de volta.
    # O @staticmethod significa que esse método pertence à classe,
    # mas não precisa de uma instância criada para ser chamado.
    # O .get("chave", valor_padrão) é uma forma segura de ler dicionários:
    # se a chave não existir (ex: arquivo antigo sem o campo), usa o padrão.
    @staticmethod
    def from_dict(dado):
        return Tarefa(
            descricao=dado["descricao"],
            prioridade=dado.get("prioridade", "baixa"),
            concluida=dado.get("concluida", False),
        )

    #LUAN MEDINA - 2024-06-17