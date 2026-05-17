## 🚀 Deploy Online
https://medalert-cli.onrender.com

# 💊 MedAlert CLI

![CI](https://github.com/JoaoCesarDev22/MedAlert-CLI/actions/workflows/ci.yml/badge.svg)

---

## 📌 Descrição

O **MedAlert CLI** é uma aplicação em linha de comando desenvolvida para auxiliar no controle de medicamentos e horários de uso, especialmente voltada para pessoas que possuem dificuldade em manter uma rotina de medicação organizada, como idosos ou pacientes em tratamento contínuo.

A aplicação permite registrar medicamentos, acompanhar horários e marcar doses como tomadas, contribuindo para a redução de esquecimentos e erros no uso de medicamentos.

---

## 🎯 Problema Real

Muitas pessoas enfrentam dificuldades em gerenciar corretamente seus medicamentos, o que pode levar a:

- Esquecimentos de doses;
- Uso incorreto dos horários;
- Riscos à saúde por má administração.

Esse problema é especialmente crítico para:

- Idosos;
- Pacientes com múltiplos medicamentos;
- Pessoas com rotinas agitadas.

---

## 💡 Solução Proposta

O **MedAlert CLI** oferece uma solução simples e acessível:

- Registro de medicamentos com nome, dosagem e horário;
- Listagem organizada dos medicamentos;
- Marcação de medicamentos como "tomados";
- Remoção de medicamentos;
- Armazenamento local em JSON (sem necessidade de banco de dados);
- Integração com API pública (OpenFDA).

---

## 👥 Público-Alvo

- Idosos;
- Cuidadores;
- Pacientes em tratamento contínuo;
- Qualquer pessoa que queira organizar melhor sua rotina de medicamentos.

---

## ⚙️ Funcionalidades

- ➕ Adicionar medicamento
- 📋 Listar medicamentos
- ✅ Marcar como tomado
- ❌ Remover medicamento
- 🌐 Consultar informações complementares via API OpenFDA

---

## 🧪 Testes Automatizados

Para rodar os testes:

```bash
python -m pytest

🔍 Lint (Qualidade de Código)
Para verificar o código com Ruff:

Bash
python -m ruff check src tests
🚀 Como Executar Localmente
1. Clonar o repositório
Bash
git clone [https://github.com/JoaoCesarDev22/MedAlert-CLI.git](https://github.com/JoaoCesarDev22/MedAlert-CLI.git)
cd MedAlert-CLI
2. Criar ambiente virtual
Bash
python -m venv venv
3. Ativar ambiente virtual (Windows PowerShell)
PowerShell
.\venv\Scripts\Activate.ps1
4. Instalar dependências
Bash
python -m pip install -r requirements.txt
5. Executar a aplicação
PowerShell
$env:PYTHONPATH="src"
python -m medalert.app
🌍 Deploy (Render)
O deploy está publicado em: https://medalert-cli.onrender.com

👨‍💻 Autor
João César Netto Souza Castro GitHub: JoaoCesarDev22

📄 Licença
Este projeto está sob a licença MIT.