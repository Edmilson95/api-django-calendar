# 🌟 Google Calendar API Integration with Django 🌟

Este projeto é uma aplicação Django que faz uma integração TOP com a API do Google Calendar, permitindo que você **crie, atualize, exclua e pesquise eventos** diretamente no seu calendário! 🚀

---

## 🚀 Começando

Estas instruções te guiarão através do processo de configuração do projeto na sua máquina local, para que você possa rodá-lo e testar suas funcionalidades.

### 📋 Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas no seu ambiente:

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- Um ambiente virtual Python configurado (explicado abaixo)
  
---

## ⚙️ Configurando o Projeto Localmente

### 1️⃣ **Clonar o Repositório**

Primeiro, você precisará clonar este repositório para o seu ambiente local:

```bash
git clone https://github.com/Edmilson95/api-django-calendar.git
cd api-django-calendar
2️⃣ Criar e Ativar o Ambiente Virtual
Agora, crie e ative um ambiente virtual para garantir que as dependências do projeto sejam isoladas:

# Criação do ambiente virtual
python -m venv venv

# Ativação no Windows
venv\Scripts\activate


3️⃣ Instalar Dependências
Com o ambiente virtual ativo, você pode instalar todas as dependências necessárias para o projeto:

pip install -r requirements.txt

4️⃣ Configurar Credenciais do Google
Para que o projeto funcione corretamente, você precisará configurar suas credenciais de OAuth 2.0 do Google.

Criando as Credenciais:
Vá para o Google Cloud Console (https://console.cloud.google.com/)
Crie um novo projeto (ou selecione um existente).
Habilite a API do Google Calendar:
Vá para "APIs e Serviços" > "Biblioteca".
Busque por "Google Calendar API" e habilite.
Crie suas credenciais OAuth 2.0:
Acesse "APIs e Serviços" > "Credenciais".
Clique em "Criar credenciais" > "ID do cliente OAuth".
Escolha o tipo de aplicativo como "Aplicativo para Desktop".
Baixe o arquivo credentials.json e coloque-o no diretório credentials/ dentro do projeto.

Configurando Variáveis de Ambiente:
Defina a variável de ambiente para apontar para o arquivo de credenciais:
set GOOGLE_CREDENTIALS_PATH=path\to\credentials.json

5️⃣ Configurar o Banco de Dados
Agora, aplique as migrações do banco de dados para criar as tabelas necessárias:
python manage.py migrate

6️⃣ Executar o Projeto Localmente
Com tudo configurado, agora você pode rodar o servidor local do Django:

python manage.py runserver

Acesse o projeto em http://localhost:8000 🎉

🔧 Funcionalidades Disponíveis
Endpoints:
POST /calendar/login/: Faz o login, retorna o token JWT.
POST /calendar/create_event/: Cria um novo evento no Google Calendar.
POST /calendar/update_event/: Atualiza um evento existente.
POST /calendar/delete_event/: Deleta um evento existente.
GET /calendar/list_events/: Lista os 10 próximos eventos no seu Calendário.
GET /calendar/list_events/: Busca eventos com base em ID, período de datas, ou título (parcial).

🧪 Testando a Aplicação
Para garantir que tudo está funcionando conforme o esperado, você pode rodar os testes automáticos que foram configurados:

python manage.py test

🛡️ Segurança
Lembre-se de que credenciais e tokens sensíveis nunca devem ser expostos no repositório. Certifique-se de que os arquivos credentials.json e token.json estão listados no seu .gitignore.

💡 Dicas Finais
Se o token de autenticação expirar, você será solicitado a autorizar novamente o acesso ao Google Calendar pela janela do navegador.
Certifique-se de que as variáveis de ambiente estejam configuradas corretamente ao rodar o projeto em ambientes de produção.

💻 Tecnologias Utilizadas
Django 4.2.7
Google Calendar API
Python 3.10
Django REST Framework

📄 Licença
Este projeto está licenciado sob a MIT License.

👨‍💻 Desenvolvido por Edmilson Ferreira