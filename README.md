Visualize a aplicação real através do link no final deste README.md.

---

## 🔹 Estrutura do projeto

```
project/
├─ app/
│   ├─ __init__.py            # screate_app()
│   ├─ config.py              # Config / env
│   ├─ extensions.py          # DB (psycopg, etc)
│   │
│   ├─ routes/
│   │   ├─ __init__.py        # regitra blueprints
│   │   ├─ pages.py           # rotas HTML
│   │   └─ api.py             # rotas REST (JSON)
│   │
│   ├─ services/              # regras de negócio
│   │   ├─ __init__.py        # pacote services (NÃO blueprint)
│   │   ├─ modelos_service.py
│   │   └─ pcp_service.py
│   │
│   ├─ repositories/          # acesso ao banco (SQL)
│   │   ├─ __init__.py        # pacote repositories
│   │   └─ modelos_repository.py
│   │
│   ├─ templates/             # Jinja2
│   │   ├─ base.html
│   │   ├─ cadastro.html
│   │   ├─ calcular.html
│   │   ├─ dashboard.html
│   │   └─ modelos.html
│   │
│   └─ static/                # arquivos estáticos
│       ├─ css/
│       │   └─ style.css
│       ├─ js/
│       │   ├─ main.js
│       │   └─ pcp.js
│       ├─ images/
│       │   ├─ banners/
│       │   ├─ logos/
│       │   └─ users/
│       └─ fonts/
│           └─ inter.woff2
│
├─ migrations/                # Alembic / Flask-Migrate
├─ tests/                     # pytest
├─ run.py                     # entrypoint da aplicação
├─ requirements.txt
├─ Procfile                   # Cloud - Railway
├─ README.md                  # Documentação principal
├─ .env                       # NÃO versionar
├─ .gitignore
└─ pyproject.toml             # opcional
```
---

## ⚙️ Tecnologias Utilizadas
* Python (Flask)
* HTML5
* CSS3
* JavaScript (Vanilla)
* Jinja2
* LocalStorage

---

## ▶️ Como Rodar o Projeto

```
1. Clonar o repositório
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. Criar e ativar o ambiente virtual
   python -m venv venv
   venv\Scripts\activate

3. Instalar as dependências
   pip install -r requirements.txt

4. Configurar variáveis de ambiente
   Crie um arquivo .env na raiz do projeto:
   FLASK_ENV=development
   SECRET_KEY=supersecretkey
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname

5. Rodar a aplicação
   python run.py

   Depois, acessar no navegador:
   http://127.0.0.1:5000
```
---

## 📌 Observações
* O sistema não utiliza login
* Os dados da compra atual ficam salvos localmente no navegador
* O cadastro de produtos é persistido no banco de dados
* Projeto ideal para uso pessoal ou familiar

---

## 👨‍💻 Autor 
Desenvolvido por Eduardo Libório
📧 eduardosoleno@protonmail.com
