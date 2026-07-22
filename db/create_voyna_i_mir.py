# create_voyna_i_mir.py
from sqlmodel import SQLModel
from db import engine
from models import Voyna_I_Mir

SQLModel.metadata.create_all(engine)
