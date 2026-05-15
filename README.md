# VitaLab
### Sistema de Gestão para Ginástica Laboral

---

## Sobre o Projeto

A ginástica laboral possui papel importante na promoção da saúde e prevenção de lesões no ambiente corporativo. Entretanto, empresas do segmento ainda enfrentam dificuldades relacionadas à organização de informações, planejamento de aulas, controle financeiro e acompanhamento das atividades realizadas.

O VitaLab foi desenvolvido com o objetivo de centralizar e otimizar os processos operacionais de empresas de ginástica laboral, oferecendo uma plataforma web moderna para gerenciamento de cadastros, cronogramas, exercícios, relatórios e controle financeiro.

O projeto foi desenvolvido como uma aplicação web utilizando Python e Flask, integrado a banco de dados relacional e controle de versão com Git e GitHub.

---

## Objetivos do Sistema

- Centralizar informações operacionais
- Facilitar o gerenciamento de empresas e professores
- Organizar cronogramas e exercícios
- Auxiliar no controle financeiro
- Gerar relatórios gerenciais
- Melhorar a produtividade e organização da empresa

---

## Funcionalidades

### Login
- Tela de autenticação do sistema
- Área de suporte rápido

### Cadastros
- Cadastro de empresas contratantes
- Cadastro de professores
- Consulta e filtros de registros
- Visualização e edição de informações

### Planejamento de Aulas
- Cadastro de exercícios
- Upload de imagens e vídeos
- Cadastro de cronogramas
- Organização de exercícios por dia

### Financeiro
- Contas a pagar
- Contas a receber
- Controle de vencimentos
- Classificação financeira

### Relatórios
- Relatórios de cadastros
- Relatórios de cronogramas
- Relatórios financeiros
- Filtros personalizados
- Impressão de relatórios

---

## Tecnologias Utilizadas

- HTML5
- CSS3
- Python
- Flask
- SQLite
- Git
- GitHub
- Font Awesome

---

## Estrutura do Projeto

```bash
VitaLab/
│
├── static/
│   └── style.css
│
├── templates/
│   │
│   ├── index.html
│   ├── dashboard.html
│   │
│   ├── cadastros.html
│   ├── novo-cadastro.html
│   ├── visualizacao-cadastro.html
│   ├── editar-cadastro.html
│   │
│   ├── planejamento.html
│   ├── exercicios.html
│   ├── cadastro-exercicio.html
│   ├── editar-exercicio.html
│   │
│   ├── cronogramas.html
│   ├── cadastro-cronograma.html
│   ├── editar-cronograma.html
│   │
│   ├── financeiro.html
│   │
│   ├── contas-pagar.html
│   ├── cadastro-conta-pagar.html
│   ├── editar-conta-pagar.html
│   │
│   ├── contas-receber.html
│   ├── cadastro-conta-receber.html
│   ├── editar-conta-receber.html
│   │
│   ├── relatorios.html
│   ├── relatorio-cadastros.html
│   ├── relatorio-cronogramas.html
│   ├── relatorio-contas-pagar.html
│   └── relatorio-contas-receber.html
│
├── README.md
├── app.py
├── requirements.txt
├── vitalab.db
│
├── criar_banco.py
├── inserir_dados.py
├── criar_tabelas_modulos.py
├── criar_relacao_cronograma.py
└── alterar_banco_professor_vinculado.py
