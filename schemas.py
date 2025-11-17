from pydantic import BaseModel
from datetime import date
from typing import Optional, Literal

# ---------- Usuário ----------
class UsuarioBase(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None
    id_grupo: int

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    id_grupo: Optional[int] = None
    senha: Optional[str] = None

class UsuarioOut(UsuarioBase):
    id_usuario: str
    class Config:
        from_attributes = True

# ---------- Horta ----------
class HortaBase(BaseModel):
    nome: str
    localizacao: str

class HortaCreate(HortaBase):
    pass

class HortaUpdate(BaseModel):
    nome: Optional[str] = None
    localizacao: Optional[str] = None

class HortaOut(HortaBase):
    id_horta: str
    data_criacao: date
    class Config:
        from_attributes = True

# ---------- Produto ----------
class ProdutoBase(BaseModel):
    nome: str
    tipo: str
    epoca_plantio: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id_produto: int
    class Config:
        from_attributes = True

# ---------- Parcela ----------
class ParcelaBase(BaseModel):
    tamanho: float
    localizacao: str
    status: Optional[str] = None

class ParcelaCreate(ParcelaBase):
    pass

class ParcelaUpdate(BaseModel):
    tamanho: Optional[float] = None
    localizacao: Optional[str] = None
    status: Optional[str] = None

class ParcelaOut(ParcelaBase):
    id_parcela: int
    class Config:
        from_attributes = True

# ---------- Evento ----------
class EventoBase(BaseModel):
    nome: str
    data_evento: date
    descricao: Optional[str] = None
    local_evento: Optional[str] = None

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    nome: Optional[str] = None
    data_evento: Optional[date] = None
    descricao: Optional[str] = None
    local_evento: Optional[str] = None

class EventoOut(EventoBase):
    id_evento: int
    class Config:
        from_attributes = True

# ---------- GruposUsuarios ----------
class GrupoCreate(BaseModel):
    nome_grupo: str
    descricao: Optional[str] = None

class GrupoOut(GrupoCreate):
    id_grupo: int
    class Config:
        from_attributes = True

# ---------- ParticipacaoEvento ----------
class ParticipacaoCreate(BaseModel):
    id_usuario: str
    id_evento: int
    papel: Literal['Participante', 'Organizador', 'Palestrante']

class ParticipacaoOut(ParticipacaoCreate):
    class Config:
        from_attributes = True

# ---------- Cultivo ----------
class CultivoCreate(BaseModel):
    id_produto: int
    id_parcela: int
    data_plantio: date
    status_cultivo: Literal['Plantado', 'Crescendo', 'ProntoParaColheita', 'Colhido']

class CultivoUpdate(BaseModel):
    status_cultivo: Optional[Literal['Plantado', 'Crescendo', 'ProntoParaColheita', 'Colhido']] = None

class CultivoOut(CultivoCreate):
    class Config:
        from_attributes = True

# ---------- Colheita ----------
class ColheitaCreate(BaseModel):
    id_parcela: int
    id_produto: int
    data_colheita: date
    quantidade_kg: float

class ColheitaOut(ColheitaCreate):
    id_colheita: int
    class Config:
        from_attributes = True
