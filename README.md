HortaWeb - Sistema de Gerenciamento de Hortas
Descrição do Projeto

O HortaWeb é um sistema web para gerenciamento de hortas, parcelas e cultivos. Ele permite:

Administradores: criar, editar e remover hortas, parcelas e cultivos, além de visualizar todos os dados do sistema.

Visitantes: apenas visualizar hortas, cultivos e produtos cadastrados.

Controle de acesso baseado em grupos de usuários (administrador ou visitante) para diferenciar permissões.

Login simples para autenticação, armazenando informações do usuário na sessão do navegador.

O projeto utiliza:

Backend: Python com FastAPI, responsável pelos endpoints e comunicação com o banco de dados.

Banco de dados: MySQL (com tabelas pré-configuradas usuarios, grupos_usuarios, hortas, produto, parcela, cultivos, colheitas, etc.).

Frontend: HTML, CSS e JavaScript, consumindo os endpoints do backend e exibindo informações conforme o tipo de usuário.

Requisitos

Python 3.10+

MySQL Server (banco de dados já configurado e populado)

Navegador moderno (Chrome, Edge, Firefox)

Conexão local com o backend rodando em http://127.0.0.1:8000

Passo a Passo para Rodar o Projeto
1. Rodando o Backend

Abra o terminal na pasta do backend (onde estão os arquivos .py).

Ative o ambiente virtual (opcional, mas recomendado):

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate


Instale as dependências (caso não estejam instaladas):

pip install fastapi uvicorn sqlalchemy mysql-connector-python pydantic


Execute o servidor FastAPI:

uvicorn main:app --reload


Verifique se o backend está rodando acessando:

http://127.0.0.1:8000/docs


Este é o Swagger UI do FastAPI, onde você pode testar os endpoints diretamente.

2. Rodando o Frontend

Abra a pasta com os arquivos login.html, hortas.html, cultivos.html e os arquivos .js correspondentes.

Abra o arquivo login.html em um navegador.

Realize login com uma das contas pré-configuradas:

Administrador

Email: admin@horta.com

Senha: 123456

Visitante

Email: visitante@horta.com

Senha: 123456

Ao fazer login, você será redirecionado para a página principal.

Dependendo do grupo do usuário, funcionalidades como criar, editar e excluir estarão habilitadas apenas para administradores.

3. Testando Permissões

Administradores podem:

Criar, editar e excluir hortas.

Criar, editar e excluir cultivos e parcelas.

Visualizar todos os registros do sistema.

Visitantes podem apenas:

Visualizar hortas, cultivos e parcelas.

Não conseguem criar, editar ou remover dados.

O frontend usa sessionStorage para armazenar o usuário logado e habilitar/desabilitar funcionalidades conforme o grupo.

4. Estrutura do Projeto
HortaWeb/
│
├─ backend/
│   ├─ main.py
│   ├─ database_mysql.py
│   ├─ models.py
│   └─ schemas.py
│
├─ frontend/
│   ├─ login.html
│   ├─ hortas.html
│   ├─ cultivos.html
│   ├─ css/
│   │   └─ style.css
│   └─ js/
│       ├─ login.js
│       ├─ hortas.js
│       └─ cultivos.js
│
└─ README.md

5. Observações

O projeto é apenas para demonstração e não deve ser usado em produção, pois a autenticação é simples e manual.

Todos os dados já devem estar carregados no banco de dados antes de executar o sistema.

Para alterar senhas ou permissões, é necessário atualizar diretamente o banco de dados.
