from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    lastname: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites_characters: Mapped[List["FavoriteCharacter"]] = relationship(
        back_populates="user")
    
    favorites_planets: Mapped[List["FavoritePlanet"]] = relationship(
        back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hair_color: Mapped[str] = mapped_column(nullable=False)
    eye_color: Mapped[str] = mapped_column(nullable=False)
    birth_year: Mapped[int] = mapped_column(nullable=False)

    favorites_characters: Mapped[List["FavoriteCharacter"]] = relationship(
        back_populates="characters")


class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    characters: Mapped["Characters"] = relationship(
        back_populates="favorites_characters")
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"), nullable=False)

    users: Mapped["User"] = relationship(back_populates="favorites_characters")
    users_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    gravity: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)

    favorites_planets: Mapped[List["FavoritePlanet"]] = relationship(
        back_populates="planets")


class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    planets: Mapped["Planets"] = relationship(back_populates="favorites_planets")
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=False)
    users: Mapped["User"] = relationship(back_populates="favorites_planets")
    users_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
