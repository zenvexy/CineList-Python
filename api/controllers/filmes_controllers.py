from fastapi import APIRouter, HTTPException

from database import database
from schema import FilmeInput


router = APIRouter(prefix="/filmes", tags=["Filmes"])


async def buscar_filme_por_id(filme_id: int):
    filme = await database.filme.find_unique(where={"id": filme_id})
    if filme is None:
        raise HTTPException(404, "Filme não encontrado")

    return filme


@router.get("/listar")
async def listar_filmes():
    return await database.filme.find_many(order={"id": "asc"})


@router.get("/buscar/{filme_id}")
async def buscar_filme(filme_id: int):
    return await buscar_filme_por_id(filme_id)


@router.post("/cadastrar", status_code=201)
async def cadastrar_filme(filme: FilmeInput):
    dados = filme.model_dump(mode="json")
    return await database.filme.create(data=dados)


@router.put("/atualizar/{filme_id}")
async def atualizar_filme(filme_id: int, filme: FilmeInput):
    await buscar_filme_por_id(filme_id)
    dados = filme.model_dump(mode="json")
    return await database.filme.update(where={"id": filme_id}, data=dados)


@router.delete("/excluir/{filme_id}")
async def excluir_filme(filme_id: int):
    await buscar_filme_por_id(filme_id)
    return await database.filme.delete(where={"id": filme_id})
