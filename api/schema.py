from pydantic import BaseModel
from prisma.enums import StatusFilme, TipoFilme


class FilmeInput(BaseModel):
    titulo: str
    tipo: TipoFilme
    genero: str
    imagem: str
    ano: int

    descricao: str | None = None
    nota: float | None = None
    status: StatusFilme = StatusFilme.PENDENTE
