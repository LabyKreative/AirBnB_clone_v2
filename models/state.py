#!/usr/bin/python3
"""Defines the state class"""
import models
import shlex
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        all_objects = models.storage.all()
        city_list = []
        result = []
        for key in all_objects:
            object_key = key.replace('.', ' ')
            object_key = shlex.split(object_key)
            if object_key[0] == 'City':
                city_list.append(all_objects[key])
        for city in city_list:
            if city.state_id == self.id:
                result.append(city)
        return result
