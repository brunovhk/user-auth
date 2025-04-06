# User Auth - Sistema de Autenticação

Este é um projeto Django focado em autenticação e registro de usuários, desenvolvido para fins educacionais.

## 🚀 Funcionalidades

- Registro de usuários
- Login/Autenticação
- Gerenciamento de sessões
- Interface responsiva

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- pipenv (gerenciador de ambientes virtuais)

## 🔧 Instalação

1. Clone o repositório:

```bash
git clone [URL_DO_SEU_REPOSITÓRIO]
cd user-auth
```

2. Instale as dependências usando pipenv:

```bash
pipenv install -r requirements.txt
```

3. Ative o ambiente virtual:

```bash
pipenv shell
```

4. Execute as migrações do banco de dados:

```bash
python manage.py migrate
```

## 🛠️ Desenvolvimento

Para rodar o projeto em ambiente de desenvolvimento:

1. Certifique-se de que está no ambiente virtual:

```bash
pipenv shell
```

2. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O servidor estará disponível em `http://localhost:8000`

## 🚀 Produção

Para configurar o projeto para produção:

1. Configure as variáveis de ambiente:

```bash
export DJANGO_SETTINGS_MODULE=UserAuth.settings.production
export SECRET_KEY=sua_chave_secreta
export DEBUG=False
```

2. Colete os arquivos estáticos:

```bash
python manage.py collectstatic
```

3. Configure um servidor WSGI (como Gunicorn):

```bash
gunicorn UserAuth.wsgi:application
```

## 📦 Estrutura do Projeto

```
user-auth/
├── accounts/           # App de autenticação
├── UserAuth/          # Configurações do projeto
├── manage.py          # Script de gerenciamento
├── requirements.txt   # Dependências do projeto
├── Pipfile           # Configuração do pipenv
└── Procfile          # Configuração para deploy
```

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
DEBUG=True
SECRET_KEY=sua_chave_secreta
DATABASE_URL=sua_url_do_banco
```

## 📝 Licença

Este projeto está sob a licença MIT.

## 👥 Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
