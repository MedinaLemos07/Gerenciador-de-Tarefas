# Gerenciador-de-Tarefas
Gerenciador de tarefas CLI em Python com persistência em JSON, organizado em camadas (models/services) e desenvolvido para aprendizado de boas práticas.

# Gerenciador de Tarefas CLI

Um gerenciador de tarefas executado diretamente pelo terminal, desenvolvido em Python puro — sem frameworks ou dependências externas.

Este projeto foi criado como parte da minha jornada de aprendizado em desenvolvimento de software, com foco em boas práticas de organização de código, estrutura em camadas e persistência de dados.

---

## Sobre o projeto

O objetivo foi construir algo funcional do zero, tomando decisões reais de arquitetura: como separar responsabilidades entre arquivos, como persistir dados de forma simples e confiável, e como estruturar um projeto Python de maneira que qualquer pessoa consiga entender e navegar.

O resultado é uma ferramenta que uso para gerenciar tarefas do dia a dia, e que representa meu entendimento atual de como escrever código limpo e bem organizado.

---

## Funcionalidades

- Adicionar tarefas com nível de prioridade (alta, média ou baixa)
- Listar tarefas ordenadas automaticamente por prioridade
- Marcar tarefas como concluídas ou reabri-las
- Editar a descrição e a prioridade de qualquer tarefa
- Remover tarefas com etapa de confirmação
- Dados salvos automaticamente em arquivo JSON a cada alteração

---

## Estrutura do projeto

```
gerenciador-tarefas/
│
├── models/
│   └── tarefa.py       # Classe Tarefa: define o formato e comportamento de uma tarefa
│
├── services/
│   └── storage.py      # Responsável por salvar e carregar dados do arquivo JSON
│
├── utils/              # Reservado para utilitários futuros
│
├── gerenciador.py      # Ponto de entrada: menu, lógica de interação e fluxo principal
└── tarefas.json        # Arquivo de dados gerado automaticamente ao adicionar tarefas
```

A separação em camadas foi uma decisão intencional: o `gerenciador.py` não sabe como os dados são salvos, e o `storage.py` não sabe como o menu funciona. Cada arquivo tem uma responsabilidade única.

---

## Como executar

Requisito: Python 3.8 ou superior instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/MedinaLemos07/Gerenciador-de-Tarefas

# 2. Acesse a pasta do projeto
cd gerenciador-tarefas

# 3. Execute
python gerenciador.py
```

---

## Demonstração

```
==========================================
        GERENCIADOR DE TAREFAS
==========================================
  [1] Adicionar tarefa
  [2] Listar tarefas
  [3] Concluir/Desconcluir tarefa
  [4] Remover tarefa
  [5] Editar tarefa
  [6] Sair
==========================================
Escolha uma opção: 2

  [✓] 1. Estudar Python        (Prioridade: alta)
  [ ] 2. Organizar repositório (Prioridade: média)
  [ ] 3. Ler documentação      (Prioridade: baixa)
```

---

## O que aprendi construindo este projeto

- Programação Orientada a Objetos com classes, atributos e métodos estáticos
- Separação de responsabilidades entre camadas do projeto
- Serialização e desserialização de dados com JSON
- Tratamento de erros com `try/except` para situações reais (arquivo inexistente, entrada inválida)
- Boas práticas Python: convenções de nomenclatura, `if __name__ == "__main__"`, imports organizados
- Como pensar em casos de falha, não só no fluxo principal

---

## Tecnologias

- Python 3
- Biblioteca padrão: `json`
