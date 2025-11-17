from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from mongo_logs import log_action
from sqlalchemy.orm import Session
from datetime import date
from fastapi.middleware.cors import CORSMiddleware

import uuid

from database_mysql import engine, Base, get_db
from models import Usuarios, Hortas, Produto, Parcela, Evento, GruposUsuarios
from models import ParticipacaoEvento as ParticipacaoEventoModel
from models import Cultivo as CultivoModel, Colheita as ColheitaModel

from schemas import (
    UsuarioCreate, UsuarioOut, UsuarioUpdate,
    HortaCreate, HortaOut, HortaUpdate,
    ProdutoCreate, ProdutoOut,
    ParcelaCreate, ParcelaOut, ParcelaUpdate,
    EventoCreate, EventoOut, EventoUpdate,
    GrupoCreate, GrupoOut,
    ParticipacaoCreate, ParticipacaoOut,
    CultivoCreate, CultivoUpdate, CultivoOut,
    ColheitaCreate, ColheitaOut
)
from auth import verificar_senha, criar_token, gerar_hash, SECRET_KEY, ALGORITHM

from jose import jwt, JWTError

app = FastAPI(title="Horta Comunitária API")

origins = [
    "http://localhost",
    "http://127.0.0.1:5500",  # a porta que você estiver servindo seu HTML
    "http://127.0.0.1:8000",  # backend local
    "*",  # desenvolvimento
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # permite POST, GET, DELETE, OPTIONS...
    allow_headers=["*"],  # permite cabeçalhos customizados
)

# criar tabelas (mantém sua linha)
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



# -----------------------
# AUTH
# -----------------------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuarios).filter(Usuarios.email == form_data.username).first()
    if not usuario or not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(400, "Usuário ou senha incorretos")
    token = criar_token({"sub": usuario.email})
    log_action("auth", "login", {"email": usuario.email})
    return {"access_token": token, "token_type": "bearer"}


def decode_token_email(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def obter_usuario_logado(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Decodifica token, busca usuário no DB e retorna o objeto Usuarios.
    Levanta HTTPException (401/404) quando apropriado.
    """
    email = decode_token_email(token)
    if not email:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    usuario = db.query(Usuarios).filter_by(email=email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario

def exigir_grupo(*grupos_permitidos: int):
    def dependency(usuario: Usuarios = Depends(obter_usuario_logado)):
        if usuario.id_grupo not in grupos_permitidos:
            raise HTTPException(status_code=403, detail="Sem permissão")
        return usuario
    return dependency



# -----------------------
# USUÁRIOS CRUD
# -----------------------
@app.post("/usuarios", response_model=UsuarioOut, status_code=201)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuarios).filter(Usuarios.email == dados.email).first():
        raise HTTPException(400, "Email já cadastrado")
    novo = Usuarios(
        id_usuario=str(uuid.uuid4()),
        nome=dados.nome,
        email=dados.email,
        telefone=dados.telefone,
        senha=gerar_hash(dados.senha),
        id_grupo=dados.id_grupo
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    log_action("usuarios", "create", {"id_usuario": novo.id_usuario, "nome": novo.nome})
    return novo

@app.put("/usuarios/{id}", response_model=UsuarioOut)
def atualizar_usuario(id: str, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    u = db.query(Usuarios).filter_by(id_usuario=id).first()
    if not u:
        raise HTTPException(404, "Usuário não encontrado")
    update_data = dados.dict(exclude_unset=True)
    if "senha" in update_data:
        update_data["senha"] = gerar_hash(update_data["senha"])
    for campo, valor in update_data.items():
        setattr(u, campo, valor)
    db.commit()
    db.refresh(u)
    log_action("usuarios", "update", {"id_usuario": u.id_usuario, "atualizado": update_data})
    return u

@app.delete("/usuarios/{id}", status_code=204)
def apagar_usuario(id: str, db: Session = Depends(get_db)):
    u = db.query(Usuarios).filter_by(id_usuario=id).first()
    if not u:
        raise HTTPException(404, "Usuário não encontrado")
    db.delete(u)
    db.commit()
    log_action("usuarios", "delete", {"id_usuario": id})
    return

@app.get("/usuarios/me", response_model=UsuarioOut)
def perfil(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = decode_token_email(token)
    if not email:
        raise HTTPException(401, "Token inválido")
    u = db.query(Usuarios).filter_by(email=email).first()
    if not u:
        raise HTTPException(404, "Usuário não encontrado")
    return u

@app.get("/usuarios", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuarios).all()

# -----------------------
# GRUPOS CRUD
# -----------------------
@app.post("/grupos", response_model=GrupoOut, status_code=201)
def criar_grupo(dados: GrupoCreate, db: Session = Depends(get_db)):
    novo = GruposUsuarios(nome_grupo=dados.nome_grupo, descricao=dados.descricao)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    log_action("grupos", "create", {"id_grupo": novo.id_grupo, "nome_grupo": novo.nome_grupo})
    return novo

@app.put("/grupos/{id}", response_model=GrupoOut)
def atualizar_grupo(id: int, dados: GrupoCreate, db: Session = Depends(get_db)):
    g = db.query(GruposUsuarios).filter_by(id_grupo=id).first()
    if not g:
        raise HTTPException(404, "Grupo não encontrado")
    g.nome_grupo = dados.nome_grupo
    g.descricao = dados.descricao
    db.commit()
    db.refresh(g)
    log_action("grupos", "update", {"id_grupo": g.id_grupo, "nome_grupo": g.nome_grupo})
    return g

@app.delete("/grupos/{id}", status_code=204)
def apagar_grupo(id: int, db: Session = Depends(get_db)):
    g = db.query(GruposUsuarios).filter_by(id_grupo=id).first()
    if not g:
        raise HTTPException(404, "Grupo não encontrado")
    db.delete(g)
    db.commit()
    log_action("grupos", "delete", {"id_grupo": id})
    return

# -----------------------
# HORTAS CRUD
# -----------------------
@app.post("/hortas", response_model=HortaOut, status_code=201)
def criar_horta(horta: HortaCreate, db: Session = Depends(get_db)):
    nova_horta = Hortas(id_horta=str(uuid.uuid4()), nome=horta.nome, localizacao=horta.localizacao, data_criacao=date.today())
    db.add(nova_horta)
    db.commit()
    db.refresh(nova_horta)
    log_action("hortas", "create", {"id_horta": nova_horta.id_horta, "nome": nova_horta.nome})
    return nova_horta

@app.put("/hortas/{id_horta}", response_model=HortaOut)
def atualizar_horta(id_horta: str, dados: HortaUpdate, db: Session = Depends(get_db)):
    h = db.query(Hortas).filter_by(id_horta=id_horta).first()
    if not h:
        raise HTTPException(404, "Horta não encontrada")
    for k, v in dados.dict(exclude_unset=True).items():
        setattr(h, k, v)
    db.commit()
    db.refresh(h)
    log_action("hortas", "update", {"id_horta": h.id_horta})
    return h

@app.delete("/hortas/{id_horta}", status_code=204)
def remover_horta(id_horta: str, db: Session = Depends(get_db)):
    h = db.query(Hortas).filter_by(id_horta=id_horta).first()
    if not h:
        raise HTTPException(404, "Horta não encontrada")
    db.delete(h)
    db.commit()
    log_action("hortas", "delete", {"id_horta": id_horta})
    return

@app.get("/hortas")
def listar_hortas(db: Session = Depends(get_db)):
    hortas = db.query(Hortas).all()
    return hortas


# -----------------------
# PRODUTOS CRUD
# -----------------------
@app.post("/produtos", response_model=ProdutoOut, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo = Produto(**produto.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    log_action("produtos", "create", {"id_produto": novo.id_produto, "nome": novo.nome})
    return novo

@app.put("/produtos/{id}", response_model=ProdutoOut)
def atualizar_produto(id: int, dados: ProdutoCreate, db: Session = Depends(get_db)):
    p = db.query(Produto).filter_by(id_produto=id).first()
    if not p:
        raise HTTPException(404, "Produto não encontrado")
    for k, v in dados.dict(exclude_unset=True).items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    log_action("produtos", "update", {"id_produto": id})
    return p

@app.delete("/produtos/{id}", status_code=204)
def remover_produto(id: int, db: Session = Depends(get_db)):
    p = db.query(Produto).filter_by(id_produto=id).first()
    if not p:
        raise HTTPException(404, "Produto não encontrado")
    db.delete(p)
    db.commit()
    log_action("produtos", "delete", {"id_produto": id})
    return

@app.get("/produtos", response_model=list[ProdutoOut])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return produtos

# -----------------------
# PARCELAS CRUD
# -----------------------
@app.post("/parcelas", response_model=ParcelaOut, status_code=201)
def criar_parcela(parcela: ParcelaCreate, db: Session = Depends(get_db)):
    nova = Parcela(**parcela.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    log_action("parcelas", "create", {"id_parcela": nova.id_parcela})
    return nova

@app.put("/parcelas/{id}", response_model=ParcelaOut)
def atualizar_parcela(id: int, dados: ParcelaUpdate, db: Session = Depends(get_db)):
    p = db.query(Parcela).filter_by(id_parcela=id).first()
    if not p:
        raise HTTPException(404, "Parcela não encontrada")
    for k, v in dados.dict(exclude_unset=True).items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    log_action("parcelas", "update", {"id_parcela": id})
    return p

@app.delete("/parcelas/{id}", status_code=204)
def remover_parcela(id: int, db: Session = Depends(get_db)):
    p = db.query(Parcela).filter_by(id_parcela=id).first()
    if not p:
        raise HTTPException(404, "Parcela não encontrada")
    db.delete(p)
    db.commit()
    log_action("parcelas", "delete", {"id_parcela": id})
    return

@app.get("/parcelas", response_model=list[ParcelaOut])
def listar_parcelas(db: Session = Depends(get_db)):
    parcelas = db.query(Parcela).all()
    return parcelas

# -----------------------
# EVENTOS CRUD
# -----------------------
@app.post("/eventos", response_model=EventoOut, status_code=201)
def criar_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    novo = Evento(**evento.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    log_action("eventos", "create", {"id_evento": novo.id_evento})
    return novo

@app.put("/eventos/{id}", response_model=EventoOut)
def atualizar_evento(id: int, dados: EventoUpdate, db: Session = Depends(get_db)):
    e = db.query(Evento).filter_by(id_evento=id).first()
    if not e:
        raise HTTPException(404, "Evento não encontrado")
    for k, v in dados.dict(exclude_unset=True).items():
        setattr(e, k, v)
    db.commit()
    db.refresh(e)
    log_action("eventos", "update", {"id_evento": id})
    return e

@app.delete("/eventos/{id}", status_code=204)
def remover_evento(id: int, db: Session = Depends(get_db)):
    e = db.query(Evento).filter_by(id_evento=id).first()
    if not e:
        raise HTTPException(404, "Evento não encontrado")
    db.delete(e)
    db.commit()
    log_action("eventos", "delete", {"id_evento": id})
    return

@app.get("/eventos")
def listar_eventos(db: Session = Depends(get_db)):
    return db.query(Evento).all()

# -----------------------
# PARTICIPACAO EVENTO (M:N)
# -----------------------
@app.post("/participacoes", response_model=ParticipacaoOut, status_code=201)
def inscrever_participacao(dados: ParticipacaoCreate, db: Session = Depends(get_db)):
    u = db.query(Usuarios).filter_by(id_usuario=dados.id_usuario).first()
    e = db.query(Evento).filter_by(id_evento=dados.id_evento).first()
    if not u or not e:
        raise HTTPException(404, "Usuário ou Evento não encontrado")
    if db.query(ParticipacaoEventoModel).filter_by(id_usuario=dados.id_usuario, id_evento=dados.id_evento).first():
        raise HTTPException(400, "Participação já registrada")
    novo = ParticipacaoEventoModel(id_usuario=dados.id_usuario, id_evento=dados.id_evento, papel=dados.papel)
    db.add(novo)
    db.commit()
    log_action("participacoes", "create", {"id_usuario": dados.id_usuario, "id_evento": dados.id_evento})
    return dados

@app.delete("/participacoes/{id_usuario}/{id_evento}", status_code=204)
def remover_participacao(id_usuario: str, id_evento: int, db: Session = Depends(get_db)):
    p = db.query(ParticipacaoEventoModel).filter_by(id_usuario=id_usuario, id_evento=id_evento).first()
    if not p:
        raise HTTPException(404, "Participação não encontrada")
    db.delete(p)
    db.commit()
    log_action("participacoes", "delete", {"id_usuario": id_usuario, "id_evento": id_evento})
    return

# -----------------------
# CULTIVOS CRUD (PK composta)
# -----------------------
@app.post("/cultivos", response_model=CultivoOut, status_code=201)
def criar_cultivo(dados: CultivoCreate, db: Session = Depends(get_db)):
    # validar existência produto/parcela
    pr = db.query(Produto).filter_by(id_produto=dados.id_produto).first()
    pa = db.query(Parcela).filter_by(id_parcela=dados.id_parcela).first()
    if not pr or not pa:
        raise HTTPException(404, "Produto ou Parcela não encontrado")
    # checar duplicidade de PK composta
    exists = db.query(CultivoModel).filter_by(
        id_produto=dados.id_produto,
        id_parcela=dados.id_parcela,
        data_plantio=dados.data_plantio
    ).first()
    if exists:
        raise HTTPException(400, "Cultivo já registrado nesta data")
    
    novo = CultivoModel(
        id_produto=dados.id_produto,
        id_parcela=dados.id_parcela,
        data_plantio=dados.data_plantio,
        status_cultivo=dados.status_cultivo
    )
    db.add(novo)
    db.commit()
    
    log_action("cultivos", "create", {
        "id_produto": dados.id_produto,
        "id_parcela": dados.id_parcela,
        "data_plantio": str(dados.data_plantio),
        "status_cultivo": dados.status_cultivo
    })
    return dados


@app.get("/cultivos", response_model=list[CultivoOut])
def listar_cultivos(db: Session = Depends(get_db)):
    rows = db.query(CultivoModel).all()
    return [
        {
            "id_produto": r.id_produto,
            "id_parcela": r.id_parcela,
            "data_plantio": r.data_plantio,
            "status_cultivo": r.status_cultivo
        } for r in rows
    ]


@app.put("/cultivos/{id_produto}/{id_parcela}/{data_plantio}", response_model=CultivoOut)
def atualizar_cultivo(id_produto: int, id_parcela: int, data_plantio: str, dados: CultivoUpdate, db: Session = Depends(get_db)):
    r = db.query(CultivoModel).filter_by(
        id_produto=id_produto,
        id_parcela=id_parcela,
        data_plantio=data_plantio
    ).first()
    if not r:
        raise HTTPException(404, "Cultivo não encontrado")
    
    update_data = dados.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(r, k, v)
    db.commit()
    
    log_action("cultivos", "update", {
        "id_produto": id_produto,
        "id_parcela": id_parcela,
        "data_plantio": data_plantio,
        **update_data
    })
    
    return {
        "id_produto": r.id_produto,
        "id_parcela": r.id_parcela,
        "data_plantio": r.data_plantio,
        "status_cultivo": r.status_cultivo
    }


@app.delete("/cultivos/{id_produto}/{id_parcela}/{data_plantio}", status_code=204)
def remover_cultivo(id_produto: int, id_parcela: int, data_plantio: str, db: Session = Depends(get_db)):
    r = db.query(CultivoModel).filter_by(
        id_produto=id_produto,
        id_parcela=id_parcela,
        data_plantio=data_plantio
    ).first()
    if not r:
        raise HTTPException(404, "Cultivo não encontrado")
    
    db.delete(r)
    db.commit()
    
    log_action("cultivos", "delete", {
        "id_produto": id_produto,
        "id_parcela": id_parcela,
        "data_plantio": data_plantio
    })
    return



# -----------------------
# COLHEITA CRUD
# -----------------------
@app.post("/colheitas", response_model=ColheitaOut, status_code=201)
def criar_colheita(dados: ColheitaCreate, db: Session = Depends(get_db)):
    # validar existência produto/parcela
    pr = db.query(Produto).filter_by(id_produto=dados.id_produto).first()
    pa = db.query(Parcela).filter_by(id_parcela=dados.id_parcela).first()
    if not pr or not pa:
        raise HTTPException(404, "Parcela ou Produto não encontrado")
    
    novo = ColheitaModel(
        id_parcela=dados.id_parcela,
        id_produto=dados.id_produto,
        data_colheita=dados.data_colheita,
        quantidade_kg=dados.quantidade_kg
    )
    db.add(novo)
    
    # atualizar status dos cultivos correspondentes
    db.query(CultivoModel).filter_by(
        id_parcela=dados.id_parcela,
        id_produto=dados.id_produto
    ).update({"status_cultivo": "Colhido"})
    
    db.commit()
    db.refresh(novo)
    
    log_action("colheitas", "create", {
        "id_parcela": dados.id_parcela,
        "id_produto": dados.id_produto,
        "data_colheita": str(dados.data_colheita),
        "quantidade_kg": float(dados.quantidade_kg)
    })
    return novo


@app.get("/colheitas", response_model=list[ColheitaOut])
def listar_colheitas(db: Session = Depends(get_db)):
    rows = db.query(ColheitaModel).all()
    return [
        {
            "id_colheita": r.id_colheita,
            "id_parcela": r.id_parcela,
            "id_produto": r.id_produto,
            "data_colheita": r.data_colheita,
            "quantidade_kg": float(r.quantidade_kg)
        } for r in rows
    ]


@app.get("/colheitas/{id}", response_model=ColheitaOut)
def buscar_colheita(id: int, db: Session = Depends(get_db)):
    c = db.query(ColheitaModel).filter_by(id_colheita=id).first()
    if not c:
        raise HTTPException(404, "Colheita não encontrada")
    return {
        "id_colheita": c.id_colheita,
        "id_parcela": c.id_parcela,
        "id_produto": c.id_produto,
        "data_colheita": c.data_colheita,
        "quantidade_kg": float(c.quantidade_kg)
    }


@app.put("/colheitas/{id}", response_model=ColheitaOut)
def atualizar_colheita(id: int, dados: ColheitaCreate, db: Session = Depends(get_db)):
    c = db.query(ColheitaModel).filter_by(id_colheita=id).first()
    if not c:
        raise HTTPException(404, "Colheita não encontrada")
    for k, v in dados.dict(exclude_unset=True).items():
        setattr(c, k, v)
    
    # atualizar status do cultivo relacionado
    db.query(CultivoModel).filter_by(
        id_parcela=c.id_parcela,
        id_produto=c.id_produto
    ).update({"status_cultivo": "Colhido"})
    
    db.commit()
    db.refresh(c)
    
    log_action("colheitas", "update", {
        "id_colheita": id,
        **dados.dict()
    })
    
    return c


@app.delete("/colheitas/{id}", status_code=204)
def remover_colheita(id: int, db: Session = Depends(get_db)):
    c = db.query(ColheitaModel).filter_by(id_colheita=id).first()
    if not c:
        raise HTTPException(404, "Colheita não encontrada")
    db.delete(c)
    db.commit()
    
    log_action("colheitas", "delete", {"id_colheita": id})
    return

