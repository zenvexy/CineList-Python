import asyncio
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from database import database


FILMES_EXEMPLO = [
    {
        "titulo": "Oppenheimer",
        "descricao": "A história do físico J. Robert Oppenheimer e do Projeto Manhattan.",
        "tipo": "FILME",
        "genero": "Drama",
        "nota": 8.1,
        "imagem": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
        "status": "ASSISTIDO",
        "ano": 2023,
    },
    {
        "titulo": "Homem-Aranha: Através do Aranhaverso",
        "descricao": "Miles Morales viaja por universos para encontrar outros heróis-Aranha.",
        "tipo": "FILME",
        "genero": "Animação",
        "nota": 8.6,
        "imagem": "https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg",
        "status": "ASSISTINDO",
        "ano": 2023,
    },
    {
        "titulo": "Parasita",
        "descricao": "Duas famílias de realidades muito diferentes se aproximam em Seul.",
        "tipo": "FILME",
        "genero": "Suspense",
        "nota": 8.5,
        "imagem": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
        "status": "PENDENTE",
        "ano": 2019,
    },
    {
        "titulo": "A Viagem de Chihiro",
        "descricao": "Uma menina atravessa um mundo espiritual para salvar seus pais.",
        "tipo": "FILME",
        "genero": "Fantasia",
        "nota": 8.6,
        "imagem": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg",
        "status": "ASSISTIDO",
        "ano": 2001,
    },
    {
        "titulo": "Duna: Parte Dois",
        "descricao": "Paul Atreides se une aos Fremen para enfrentar a Casa Harkonnen.",
        "tipo": "FILME",
        "genero": "Ficção científica",
        "nota": 8.5,
        "imagem": "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg",
        "status": "PENDENTE",
        "ano": 2024,
    },
]


async def main() -> None:
    await database.connect()
    try:
        for dados in FILMES_EXEMPLO:
            existente = await database.filme.find_first(
                where={
                    "titulo": dados["titulo"],
                    "tipo": dados["tipo"],
                    "ano": dados["ano"],
                }
            )
            if existente is None:
                await database.filme.create(data=dados)
        print("Filmes de exemplo disponíveis.")
    finally:
        await database.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
