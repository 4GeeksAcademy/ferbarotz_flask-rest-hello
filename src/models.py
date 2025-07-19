from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column,  relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    apellido: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    subcripcion: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    planetas = relationship("Planeta", back_populates="user")
    personajes = relationship("Personaje", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "password": self.password,
            "subcripcion": self.subcripcion,
            # do not serialize the password, its a security breach
        }
# PLANETA

class Planeta (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    planeta: Mapped[str] = mapped_column(nullable=False)
    terreno: Mapped[str] = mapped_column(nullable=False)
    poblacion: Mapped[int] = mapped_column(Integer,nullable=False)
    

    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="planetas")

    
    planetafavs = relationship("Planetafav", back_populates="planeta")

   
    def serialize(self):
        return {
            "id": self.id,
            "planeta": self.planeta,
            "terreno": self.terreno,
            "poblacion": self.poblacion
            
            # do not serialize the password, its a security breach
        }
    
# PERSONAJE

class Personaje(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    personaje: Mapped[str] = mapped_column(nullable=False)
    peso: Mapped[int] = mapped_column(Integer,nullable=False)
    ojos: Mapped[str] = mapped_column(nullable=False)
    

    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="personajes")

    personajefav = relationship("Personajefav", back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "personaje": self.personaje,
            "peso": self.peso,
            "ojos": self.ojos,
            # do not serialize the password, its a security breach
        }
    
# PLANETA_FAVORITO

class Planetafav(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(primary_key=True)
    planeta_id: Mapped[int] = mapped_column(primary_key=True)
  
    planeta_id = mapped_column(ForeignKey("planeta.id"))
    planeta = relationship("Planeta", back_populates="planetafavs")

    user_id = mapped_column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="planetafavs")

    empresa_id = mapped_column(ForeignKey("empresa.id"))
    empresa = relationship("Empresa", back_populates="planetafavs")
    
    def serialize(self):
        return {
            "id": self.id,
            "planeta_id": self.planeta_id,
            "user_id": self.user_id,
            "id_favorito": self.id_favorito,
            # do not serialize the password, its a security breach
        }
    
# PERSONAJE_FAVORITO

class Personajefav(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(primary_key=True)
    personaje_id: Mapped[int] = mapped_column(primary_key=True)

    personaje_id = mapped_column(ForeignKey("personaje.id"))
    personaje = relationship("Personaje", back_populates="personajefav") 
   
    user_id = mapped_column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="personajefavs")

    empresa_id = mapped_column(ForeignKey("empresa.id"))
    empresa = relationship("Empresa", back_populates="personajefavs")

    def serialize(self):
        return {
            "id": self.id,
            "personaje_id": self.personaje_id,
            "user_id": self.user_id,
            "id_favorito": self.id_favorito,
            # do not serialize the password, its a security breach
        }
    
       

class Empresa(db.Model):
        id: Mapped[int] = mapped_column(primary_key=True)
        nombre: Mapped[str] = mapped_column(String(120), nullable=False)
        ciudad: Mapped[str] = mapped_column(nullable=False)
        slogan: Mapped[str] = mapped_column(nullable=False) 

        planetafavs = relationship("Planetafav", back_populates="empresa")
        personajefavs = relationship("Personajefav", back_populates="empresa")
        
        videojuego = relationship("Videojuego", back_populates="empresa")
        

        def serialize(self):
            return {
              "id": self.id,
             "nombre": self.nombre,
             "ciudad": self.ciudad,
             "slogan": self.slogan
            }
        def _str_(self):
            return self.nombre

class Videojuego(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    genero: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[str] = mapped_column(nullable=False) 

    empresa_id= mapped_column(ForeignKey("empresa.id"))
    empresa = relationship("Empresa", back_populates="videojuego")

    def serialize(self):
            return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            # do not serialize the password, its a security breach
        }

