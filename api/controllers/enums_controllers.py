from fastapi import APIRouter

from schema import StatusFilme, TipoFilme


router = APIRouter(prefix="/enums", tags=["Enums"])


@router.get("/tipos-filme/listar")
async def listar_tipos_filme() -> list[str]:
    return [tipo.value for tipo in TipoFilme]


@router.get("/status-filme/listar")
async def listar_status_filme() -> list[str]:
    return [status.value for status in StatusFilme]
