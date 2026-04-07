# Esse é o arquivo principal do projeto. Aqui ficam todas as funções
# que o usuário aciona pelo menu, além do loop que mantém o programa rodando.

from models.tarefa import Tarefa
from services.storage import carregar_tarefas, salvar_tarefas


# ─────────────────────────────────────────────────────────────────────────────
# Funções auxiliares — usadas internamente pelas funções do menu
# ─────────────────────────────────────────────────────────────────────────────

def ordenar_tarefas(tarefas):
    # Defino manualmente a ordem das prioridades usando um dicionário.
    # O sorted() vai usar esse número como critério: menor número = aparece primeiro.
    # O .get(t.prioridade, 3) é uma proteção: se a prioridade for desconhecida,
    # ela vai para o final da lista (posição 3).
    ordem = {"alta": 0, "média": 1, "baixa": 2}
    return sorted(tarefas, key=lambda t: ordem.get(t.prioridade, 3))


def pedir_prioridade():
    # Fico pedindo até o usuário digitar uma opção válida.
    # O .strip() remove espaços acidentais antes e depois do texto digitado.
    # O .lower() converte para minúsculas, então "Alta", "ALTA" e "alta" funcionam igual.
    while True:
        prioridade = input("Qual a prioridade da tarefa? (alta/média/baixa): ").strip().lower()

        if prioridade in ("alta", "media", "média", "baixa"):
            # Aceito "media" sem acento também para facilitar a digitação,
            # mas internamente padronizo sempre como "média".
            if prioridade == "media":
                prioridade = "média"
            return prioridade

        print("Prioridade inválida! Escolha entre: alta, média ou baixa.")


def pedir_numero_tarefa(tarefas, acao="selecionar"):
    # Essa função centraliza a lógica de pedir um número ao usuário
    # e traduzi-lo para o índice correto na lista original.
    #
    # Por que isso é necessário?
    # A lista é EXIBIDA ordenada por prioridade, mas é ARMAZENADA na ordem
    # em que as tarefas foram criadas. Se eu usasse o número que o usuário
    # digitou direto como índice, poderia alterar a tarefa errada.
    # A solução: pego a tarefa correta na lista ordenada e depois localizo
    # ela na lista original com .index().

    listar_tarefas(tarefas)

    try:
        numero = int(input(f"Qual tarefa deseja {acao}? "))
        indice_exibido = numero - 1  # O usuário conta a partir de 1, Python conta a partir de 0

        tarefas_ordenadas = ordenar_tarefas(tarefas)

        if not (0 <= indice_exibido < len(tarefas_ordenadas)):
            print("Tarefa não existe!")
            return None

        # Identifico qual objeto Tarefa corresponde ao número que o usuário viu na tela...
        tarefa_escolhida = tarefas_ordenadas[indice_exibido]

        # ...e descubro em qual posição esse mesmo objeto está na lista original.
        # Isso funciona porque .index() compara por identidade de objeto (memória),
        # então sempre acha o objeto certo.
        indice_original = tarefas.index(tarefa_escolhida)
        return indice_original

    except ValueError:
        # Cai aqui se o usuário digitar algo que não seja número (ex: "abc").
        print("Número inválido! Por favor, tente novamente.")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Funções do menu — cada opção do menu tem sua própria função
# ─────────────────────────────────────────────────────────────────────────────

def listar_tarefas(tarefas):
    if not tarefas:  # Forma pythônica de checar se a lista está vazia
        print("Nenhuma tarefa cadastrada.")
        return

    # Exibo sempre na ordem de prioridade, independente da ordem de criação.
    tarefas_ordenadas = ordenar_tarefas(tarefas)

    print()
    for numero, tarefa in enumerate(tarefas_ordenadas, start=1):
        # enumerate() me dá o índice e o item ao mesmo tempo.
        # start=1 faz a contagem começar em 1 em vez de 0, que é mais natural pro usuário.
        status = "✓" if tarefa.concluida else " "
        print(f"  [{status}] {numero}. {tarefa.descricao} (Prioridade: {tarefa.prioridade})")
    print()


def adicionar_tarefa(tarefas):
    descricao = input("Digite a nova tarefa: ").strip()

    # Não faz sentido salvar uma tarefa com descrição vazia.
    if not descricao:
        print("A descrição não pode estar vazia!")
        return

    prioridade = pedir_prioridade()

    tarefa = Tarefa(descricao, prioridade)  # Crio o objeto usando a classe do models/
    tarefas.append(tarefa)                  # Adiciono na lista que está na memória
    salvar_tarefas(tarefas)                 # Persisto a lista atualizada no arquivo JSON
    print(f"Tarefa '{descricao}' adicionada com sucesso!")


def concluir_tarefa(tarefas):
    # Uso a função auxiliar para obter o índice correto na lista original.
    indice = pedir_numero_tarefa(tarefas, acao="concluir/desconcluir")

    if indice is None:  # O usuário digitou algo inválido — a função auxiliar já avisou
        return

    # O "not" inverte o valor booleano: se era True vira False, se era False vira True.
    # Isso permite concluir E desconcluir com a mesma lógica.
    tarefas[indice].concluida = not tarefas[indice].concluida

    estado = "concluída" if tarefas[indice].concluida else "marcada como pendente"
    print(f"Tarefa '{tarefas[indice].descricao}' {estado}!")
    salvar_tarefas(tarefas)


def remover_tarefa(tarefas):
    indice = pedir_numero_tarefa(tarefas, acao="remover")

    if indice is None:
        return

    # Peço confirmação antes de remover — ação irreversível merece uma verificação extra.
    while True:
        confirmar = input("Tem certeza que deseja remover essa tarefa? (s/n): ").strip().lower()

        if confirmar == "s":
            # .pop(indice) remove o item naquela posição E o retorna,
            # permitindo que eu use a descrição na mensagem de confirmação.
            removida = tarefas.pop(indice)
            salvar_tarefas(tarefas)
            print(f"Tarefa '{removida.descricao}' removida com sucesso!")
            break

        elif confirmar == "n":
            print("Remoção cancelada.")
            break

        else:
            # Se não for "s" nem "n", volto ao início do loop e pergunto de novo.
            print("Opção inválida! Digite 's' para confirmar ou 'n' para cancelar.")


def editar_tarefa(tarefas):
    indice = pedir_numero_tarefa(tarefas, acao="editar")

    if indice is None:
        return

    # Se o usuário apertar Enter sem digitar nada, mantenho a descrição atual.
    nova_descricao = input("Nova descrição (Enter para manter a atual): ").strip()
    if nova_descricao:
        tarefas[indice].descricao = nova_descricao

    mudar = input("Deseja alterar a prioridade? (s/n): ").strip().lower()

    if mudar == "s":
        tarefas[indice].prioridade = pedir_prioridade()
    elif mudar != "n":
        print("Opção inválida! A prioridade não foi alterada.")

    salvar_tarefas(tarefas)
    print("Tarefa atualizada com sucesso!")


# ─────────────────────────────────────────────────────────────────────────────
# Menu e ponto de entrada
# ─────────────────────────────────────────────────────────────────────────────

def exibir_menu():
    # Separei o menu em sua própria função para manter o main() limpo.
    # Se eu quiser mudar o visual do menu, sei exatamente onde vir.
    print("==========================================")
    print("        GERENCIADOR DE TAREFAS")
    print("==========================================")
    print("  [1] Adicionar tarefa")
    print("  [2] Listar tarefas")
    print("  [3] Concluir/Desconcluir tarefa")
    print("  [4] Remover tarefa")
    print("  [5] Editar tarefa")
    print("  [6] Sair")
    print("==========================================")


def main():
    # Carrego as tarefas do arquivo JSON uma vez ao iniciar.
    # A partir daí, trabalho com a lista em memória e salvo sempre que houver mudança.
    tarefas = carregar_tarefas()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_tarefa(tarefas)

        elif opcao == "2":
            listar_tarefas(tarefas)

        elif opcao == "3":
            if not tarefas:
                print("Nenhuma tarefa cadastrada.")
            else:
                concluir_tarefa(tarefas)

        elif opcao == "4":
            if not tarefas:
                print("Nenhuma tarefa cadastrada.")
            else:
                remover_tarefa(tarefas)

        elif opcao == "5":
            if not tarefas:
                print("Nenhuma tarefa cadastrada.")
            else:
                editar_tarefa(tarefas)

        elif opcao == "6":
            print("Encerrando o gerenciador de tarefas. Até mais!")
            break

        else:
            print("Opção inválida! Por favor, escolha uma opção entre 1 e 6.")


# Esse bloco garante que o main() só rode quando eu executar esse arquivo diretamente.
# Se outro arquivo importar o gerenciador.py (ex: um script de testes),
# o menu NÃO vai abrir automaticamente — o importador decide o que usar.
if __name__ == "__main__":
    main()


#LUAN MEDINA - 2024-06-17