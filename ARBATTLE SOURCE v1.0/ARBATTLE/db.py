# -*- coding: latin1 -*-
import os
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

path = os.path.dirname(os.path.abspath(__file__))
engine = create_engine('sqlite:///'+path+'/db/db.sqlite', module=sqlite)

Base = declarative_base(bind=engine)


#cria as classes e tabelas ja mapeando
class Carta(Base):
    __tablename__ = 'carta'

    id = Column(Integer, primary_key=True)
    nome = Column(String(20), nullable=False)    
    ataque = Column(Integer, nullable=False)
    defesa = Column(Integer, nullable=False)
    classe = Column(Integer, nullable=False)
    pattern = Column(String(50), nullable=False)
    egg    = Column(String(50), nullable=False)
    tamanho = Column(Integer, nullable=False)
    ativo = Column(Boolean, nullable=False)
    
    
    
    def __init__(self, nome, ataque, defesa, classe, pattern, egg, tamanho, ativo=True):
        self.nome = nome
        self.ataque = ataque
        self.defesa = defesa
        self.classe = classe
        self.pattern = pattern
        self.egg = egg
        self.ativo = ativo
        self.tamanho = tamanho
        

    def __repr__(self):
        return "%s (A = %i, D = %i, C = %i)" % (self.nome, self.ataque, self.defesa, self.classe)
    

Base.metadata.create_all()
Session = sessionmaker(bind=engine)


