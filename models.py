from sqlalchemy import func, Text, Column, Integer, String, CHAR, ForeignKey, Date, text, Enum, Float
from sqlalchemy.orm import relationship
from database_mysql import Base
import uuid

class GruposUsuarios(Base):
    __tablename__ = 'grupos_usuarios'
    id_grupo = Column(Integer, primary_key=True)
    nome_grupo = Column(String(50))
    descricao = Column(String(200))
    usuarios = relationship("Usuarios", back_populates="grupo")

class Usuarios(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(CHAR(36), primary_key=True)
    id_grupo = Column(Integer, ForeignKey("grupos_usuarios.id_grupo"))
    nome = Column(String(100))
    email = Column(String(100))
    telefone = Column(String(20))
    senha = Column(String(255), nullable=False)


    grupo = relationship("GruposUsuarios", back_populates="usuarios")




class Hortas(Base):
    __tablename__ = 'hortas'

    id_horta = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False)
    localizacao = Column(String(255), nullable=False)
    data_criacao = Column(Date, server_default=func.curdate())

class Produto(Base):
    __tablename__ = "produto"

    id_produto = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(Enum("Verdura", "Legume", "Fruta", "Hortaliça"), nullable=False)
    epoca_plantio = Column(String(50))


class Parcela(Base):
    __tablename__ = "parcela"

    id_parcela = Column(Integer, primary_key=True, autoincrement=True)
    tamanho = Column(Float, nullable=False)
    localizacao = Column(String(100), nullable=False)
    status = Column(Enum("Livre", "Cultivando", "Em Repouso"), default="Livre")

class Evento(Base):
    __tablename__ = "evento"

    id_evento = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    data_evento = Column(Date, nullable=False)
    descricao = Column(Text)
    local_evento = Column(String(100))

class ParticipacaoEvento(Base):
    __tablename__ = 'ParticipacaoEvento'
    id_usuario = Column(CHAR(36), ForeignKey('usuarios.id_usuario'), primary_key=True)
    id_evento = Column(Integer, ForeignKey('evento.id_evento'), primary_key=True)
    papel = Column(Enum('Participante', 'Organizador', 'Palestrante', name='papel_enum'), nullable=False)

class Cultivo(Base):
    __tablename__ = "cultivos"
    id_produto = Column(Integer, ForeignKey("produto.id_produto"), primary_key=True)
    id_parcela = Column(Integer, ForeignKey("parcela.id_parcela"), primary_key=True)
    data_plantio = Column(Date, primary_key=True)
    status_cultivo = Column(String(50))

class Colheita(Base):
    __tablename__ = "colheitas"
    id_colheita = Column(Integer, primary_key=True, autoincrement=True)
    id_parcela = Column(Integer, ForeignKey("parcela.id_parcela"))
    id_produto = Column(Integer, ForeignKey("produto.id_produto"))
    data_colheita = Column(Date)
    quantidade_kg = Column(Float)