# CineList - Backend

Aplicação local para gerenciar filmes e séries. O backend usa FastAPI, Prisma Client Python e PostgreSQL no NeonDB.

## Complementar

Este readme é um complementar do [Frontend](./web/README.md)

## Pré-requisitos

- Windows e CMD.
- Python 3.13 instalado e disponível pelo comando `py`.
- Node.js instalado, necessário para o Prisma CLI.
- Conta no [Neon](https://neon.tech/).
- VS Code (opcional).

## Banco de dados

1. Acesse [console.neon.tech](https://console.neon.tech/) e entre na sua conta.
2. Clique em **New Project** para criar um banco PostgreSQL.
3. Abra o projeto criado e clique em **Connect**.
4. Selecione **Direct connection** e copie a URL exibida.
5. No CMD, entre na pasta da API:

   ```cmd
   cd api
   ```

6. Crie o arquivo `.env`

7. Adicione a URL copiada do Neon no formato abaixo e salve o arquivo:

   ```env
   DATABASE_URL="postgresql://usuario:senha@host/neondb?sslmode=require"
   ```

   Troque o valor de exemplo pela URL completa copiada do Neon. O arquivo `.env` guarda a senha do banco e não deve ser enviado ao Git.

## Instalar e iniciar o backend

No CMD, ainda dentro da pasta `api`, crie e ative o ambiente virtual:

```cmd
py -3.13 -m venv .venv
.venv\Scripts\activate.bat
```

Instale as dependências:

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Valide o schema, gere o cliente Prisma e crie as tabelas no Neon:

```cmd
prisma validate
prisma generate
prisma db push
```

Opcionalmente, adicione filmes e séries de exemplo:

```cmd
python prisma\seed.py
```

O seed adiciona os filmes abaixo quando eles ainda não existem no banco. Cada registro inclui uma URL pública para a imagem da capa:

- Oppenheimer
- Homem-Aranha: Através do Aranhaverso
- Parasita
- A Viagem de Chihiro
- Duna: Parte Dois

Inicie a API:

```cmd
python -m uvicorn app:app --reload
```

Mantenha essa janela do CMD aberta enquanto usar a API. A documentação interativa fica em `http://127.0.0.1:8000/docs`.

## Publicar na Vercel

1. Envie o projeto para um repositório no GitHub.
2. Na Vercel, clique em **Add New → Project** e importe o repositório.
3. Em **Root Directory**, clique em **Edit** e escolha a pasta `api`.
4. Em **Environment Variables**, crie a variável `DATABASE_URL` e cole a mesma URL do Neon usada no arquivo `.env`.
5. Clique em **Deploy**.

A Vercel usa a pasta definida em **Root Directory** como a raiz do backend. Como essa pasta é `api`, ela encontra e instala as bibliotecas listadas em `api/requirements.txt` com `pip`.

Depois, ela encontra o arquivo `api/app.py` e a variável `app`, que é a aplicação FastAPI. Antes da publicação, o `api/pyproject.toml` manda executar `api/build.py`; esse script gera o Prisma Client necessário para a conexão com o banco Neon.

As rotas publicadas usam o prefixo `/api`, por exemplo:

```text
https://seu-projeto.vercel.app/api/filmes/listar
```

Não é necessário criar `vercel.json` para redirecionar as rotas.

## Usar a interface web

Com o backend publicado, abra o terminal na pasta raiz do projeto e inicie um servidor local para os arquivos da interface:

```cmd
python -m http.server 5500
```

Acesse `http://localhost:5500`. A interface em `web/filmes.html` usa a API publicada em `https://cinelist-backend.vercel.app` para listar, cadastrar, editar e excluir filmes e séries. O uso da porta `5500` corresponde às origens locais permitidas pelo CORS do backend.

## License

Este projeto é licenciado sob a [Apache License 2.0](./LICENSE).
