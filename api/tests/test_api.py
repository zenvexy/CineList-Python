import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient


PASTA_API = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA_API))


class FilmeRepositoryFake:
    def __init__(self):
        self.registros = {}
        self.proximo_id = 1

    async def find_many(self, *, order):
        return [self.registros[filme_id] for filme_id in sorted(self.registros)]

    async def find_unique(self, *, where):
        return self.registros.get(where["id"])

    async def create(self, *, data):
        registro = {"id": self.proximo_id, **data}
        self.registros[self.proximo_id] = registro
        self.proximo_id += 1
        return registro

    async def update(self, *, where, data):
        self.registros[where["id"]].update(data)
        return self.registros[where["id"]]

    async def delete(self, *, where):
        return self.registros.pop(where["id"])


class DatabaseFake:
    def __init__(self):
        self.filme = FilmeRepositoryFake()

    async def connect(self):
        pass

    async def disconnect(self):
        pass


database = DatabaseFake()
modulo_database = types.ModuleType("database")
modulo_database.database = database

with patch.dict(sys.modules, {"database": modulo_database}):
    from app import app


class APITest(unittest.TestCase):
    def setUp(self):
        database.filme = FilmeRepositoryFake()
        self.client = TestClient(app)

    def test_crud_filmes_e_nao_encontrado(self):
        filme = {
            "titulo": "Filme de teste",
            "tipo": "FILME",
            "genero": "Aventura",
            "imagem": "/imagens/filme-de-teste.jpg",
            "ano": 2024,
        }
        criado = self.client.post("/api/filmes/cadastrar", json=filme)
        self.assertEqual(criado.status_code, 201)
        self.assertEqual(criado.json()["status"], "PENDENTE")
        self.assertEqual(
            self.client.get("/api/filmes/listar").json()[0]["titulo"], filme["titulo"]
        )
        self.assertEqual(self.client.get("/api/filmes/buscar/1").json()["id"], 1)

        atualizado = self.client.put(
            "/api/filmes/atualizar/1",
            json={**filme, "status": "ASSISTIDO", "nota": 8.0},
        )
        self.assertEqual(atualizado.status_code, 200)
        self.assertEqual(atualizado.json()["status"], "ASSISTIDO")

        self.assertEqual(self.client.delete("/api/filmes/excluir/1").status_code, 200)
        self.assertEqual(self.client.get("/api/filmes/buscar/1").status_code, 404)

    def test_enums_somente_listagem_e_validacao(self):
        self.assertEqual(
            self.client.get("/api/enums/tipos-filme/listar").json(), ["FILME", "SERIE"]
        )
        self.assertEqual(
            self.client.get("/api/enums/status-filme/listar").json(),
            ["PENDENTE", "ASSISTIDO", "ASSISTINDO"],
        )
        self.assertEqual(self.client.post("/api/enums/tipos-filme/listar").status_code, 405)
        self.assertEqual(
            self.client.post(
                "/api/filmes/cadastrar",
                json={
                    "titulo": "Inválido",
                    "tipo": "LIVRO",
                    "genero": "Drama",
                    "imagem": "/imagens/invalido.jpg",
                    "ano": 2024,
                },
            ).status_code,
            422,
        )


if __name__ == "__main__":
    unittest.main()
