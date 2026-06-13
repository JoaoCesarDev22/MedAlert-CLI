# 💊 MedAlert CLI

[![CI](https://github.com/JoaoCesarDev22/MedAlert-CLI/actions/workflows/ci.yml/badge.svg)](https://github.com/JoaoCesarDev22/MedAlert-CLI/actions/workflows/ci.yml)

---

## 📌 Descrição

O **MedAlert CLI** é uma aplicação robusta que une a praticidade de uma interface de linha de comando (CLI) à escalabilidade de uma arquitetura baseada em microsserviços na nuvem. Desenvolvido para auxiliar no controle de medicamentos e horários de uso, o sistema é voltado para pessoas que possuem dificuldade em manter uma rotina de medicação organizada, como idosos, cuidadores ou pacientes em tratamento contínuo.

A aplicação permite registrar medicamentos, acompanhar horários e marcar doses como tomadas, reduzindo drasticamente o risco de esquecimentos e erros de administração.

---

## 🚀 Deploy Online & Arquitetura

A aplicação está conteinerizada e hospedada em ambiente de produção na nuvem:

* **API Server (Render):** https://medalert-cli.onrender.com
* **Banco de Dados Relacional:** Supabase (PostgreSQL Cloud)

---

## 💡 Evolução do Projeto (Novas Funcionalidades)

O projeto evoluiu de um protótipo local para uma aplicação cliente-servidor distribuída:

- **Persistência na Nuvem (Supabase):** Substituição do armazenamento local em arquivos JSON por um banco de dados relacional PostgreSQL robusto hospedado no Supabase.
- **Arquitetura API REST (Flask):** Desacoplamento da lógica de negócios. O cliente CLI consome uma API Flask centralizada.
- **Integração com API Externa (OpenFDA):** Consulta em tempo real a dados de segurança e bulas de medicamentos diretamente da base oficial norte-americana.
- **Infraestrutura como Código (Docker):** Dockerfile otimizado com injeção de paths dinâmicos para deploy imediato.

---

## 👥 Público-Alvo e Problema Real

Muitas pessoas enfrentam dificuldades em gerenciar múltiplos medicamentos, gerando esquecimentos de doses e riscos de toxicidade por horários incorretos. O MedAlert CLI foca em fornecer uma barreira de segurança simples para:

- Idosos e cuidadores;
- Pacientes crônicos com polimedicação;
- Pessoas com rotinas dinâmicas.

---

## ⚙️ Funcionalidades Operacionais

- ➕ **Adicionar Medicamento:** Registro de nome, dosagem e horário com validação de formato de tempo.
- 📋 **Listar Medicamentos:** Exibição sincronizada direto do banco de dados em nuvem.
- ✅ **Marcar como Tomado:** Atualização de status em tempo real.
- ❌ **Remover Medicamento:** Limpeza de registros da base relacional.
- 🌐 **Consultar OpenFDA:** Consulta de informações farmacológicas complementares via requisições HTTP (`requests`).

---

## 🚀 Como Executar o Projeto Localmente

Siga o passo a passo abaixo para configurar o ambiente de desenvolvimento em sua máquina.

### 1. Clonar o Repositório

```bash
git clone https://github.com/JoaoCesarDev22/MedAlert-CLI.git
cd MedAlert-CLI
```

### 2. Configurar o Ambiente Virtual (Python 3.11+)

```bash
python -m venv venv
```

Ativar o ambiente virtual:

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Instalar as Dependências do Sistema

O arquivo de requisitos foi normalizado em UTF-8 e inclui os drivers nativos do PostgreSQL (`psycopg2-binary`) e clientes HTTP (`requests`):

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com a string de conexão do banco PostgreSQL (Supabase):

```env
DATABASE_URL=postgresql://usuario:senha@host:porta/postgres
```

### 5. Inicializar o Servidor da API (Flask)

Para que a API responda às requisições, o servidor local (ou de produção) precisa estar rodando:

```powershell
# Definir o caminho de busca do Python
$env:PYTHONPATH="src"

# Iniciar o servidor
python -m medalert.server
```

### 6. Executar a Aplicação CLI (em outro terminal)

Com o servidor rodando, abra uma nova aba de terminal, ative o `venv` e execute o cliente:

```powershell
$env:PYTHONPATH="src"
python -m medalert.app
```

---

## 🧪 Suíte de Testes Automatizados e Qualidade

O projeto conta com testes unitários e de integração integrados ao pipeline de CI do GitHub Actions para garantir o funcionamento das rotas da API e serviços.

**Executar testes com Pytest:**

```bash
python -m pytest -v
```

**Verificar qualidade de código (Lint com Ruff):**

```bash
python -m ruff check src tests
```

---

## 👨‍💻 Autores (Contribuição em Grupo)

Projeto desenvolvido em colaboração acadêmica por:

- **João César Netto Souza Castro** ([@JoaoCesarDev22](https://github.com/JoaoCesarDev22)) — Gerenciamento de Infraestrutura de CI/CD, Arquitetura Base da API e Branches.
- **Hélio de Almeida** ([@Helio965](https://github.com/Helio965)) — Ajustes de Deploy, Resolução de Dependências da CI (`requests`/`psycopg2`), Normalização de Encodings e Refatoração de Contêineres.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
