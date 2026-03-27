# 💊 MedAlert CLI

![CI](https://github.com/JoaoCesarDev22/MedAlert-CLI/actions/workflows/ci.yml/badge.svg)

## 📌 Descrição

O **MedAlert CLI** é uma aplicação simples em linha de comando desenvolvida para auxiliar no controle de medicamentos e horários de uso, especialmente voltada para pessoas que possuem dificuldade em manter uma rotina de medicação organizada, como idosos ou pacientes com tratamentos contínuos.

A aplicação permite registrar medicamentos, acompanhar horários e marcar doses como tomadas, contribuindo para a redução de esquecimentos e erros no uso de medicamentos.

---

## 🎯 Problema Real

Muitas pessoas enfrentam dificuldades em gerenciar corretamente seus medicamentos, o que pode levar a:

* esquecimentos de doses;
* uso incorreto de horários;
* riscos à saúde por má administração.

Esse problema é especialmente crítico para:

* idosos;
* pacientes com múltiplos medicamentos;
* pessoas com rotinas agitadas.

---

## 💡 Solução Proposta

O MedAlert CLI oferece uma solução simples e acessível:

* registro de medicamentos com nome, dosagem e horário;
* listagem organizada dos medicamentos;
* marcação de medicamentos como "tomados";
* remoção de medicamentos;
* armazenamento local em JSON (sem necessidade de banco de dados).

---

## 👥 Público-Alvo

* idosos;
* cuidadores;
* pacientes em tratamento contínuo;
* qualquer pessoa que queira organizar melhor sua rotina de medicamentos.

---

## ⚙️ Funcionalidades

* ➕ Adicionar medicamento
* 📋 Listar medicamentos
* ✅ Marcar como tomado
* ❌ Remover medicamento
* 💾 Persistência em arquivo JSON

---

## 🛠️ Tecnologias Utilizadas

* Python 3.14
* Pytest (testes automatizados)
* Ruff (linting/análise estática)
* Git & GitHub
* GitHub Actions (CI/CD)

---

## 📂 Estrutura do Projeto

```
medalert-cli/
├── src/
│   └── medalert/
│       ├── app.py
│       ├── models.py
│       ├── services.py
│       └── storage.py
├── tests/
│   ├── test_services.py
│   └── test_storage.py
├── .github/workflows/ci.yml
├── requirements.txt
├── pytest.ini
├── VERSION
└── README.md
```

---

## 🚀 Como Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/JoaoCesarDev22/MedAlert-CLI.git
cd MedAlert-CLI
```

### 2. Instalar dependências

```bash
python -m pip install -r requirements.txt
```

### 3. Executar a aplicação

```bash
python src/medalert/app.py
```

---

## 🧪 Testes Automatizados

Para rodar os testes:

```bash
python -m pytest
```

---

## 🔍 Lint (Qualidade de Código)

Para verificar o código:

```bash
python -m ruff check src tests
```

---

## 🔄 Integração Contínua (CI)

O projeto utiliza **GitHub Actions** para:

* instalar dependências;
* rodar lint;
* executar testes automaticamente a cada push.

Status atual:

✔ Build automatizado ativo
✔ Testes validados automaticamente

---

## 📦 Versionamento

Este projeto segue o padrão de versionamento semântico:

```
MAJOR.MINOR.PATCH
```

Versão atual:

```
1.0.0
```

---

## 📸 Exemplo de Uso

```
1. Adicionar medicamento
2. Listar medicamentos
3. Marcar como tomado
4. Remover medicamento
5. Sair
```

---

## 👨‍💻 Autor

**João César**

GitHub:
https://github.com/JoaoCesarDev22

---

## 📄 Licença

Este projeto está sob a licença MIT.
