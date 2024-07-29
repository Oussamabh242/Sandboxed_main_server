
import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
import uuid

# Get the directory path of the current script
base_dir = os.path.abspath(os.path.dirname(__file__))
# Construct the path to the database file
database_path = os.path.join(base_dir, 'problems.db')

# SQLAlchemy setup
db = SQLAlchemy()

class Base(DeclarativeBase):
    pass

class Problem(Base):
    __tablename__ = 'problems'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    constraints: Mapped[str] = mapped_column(String, nullable=False)
    difficulty: Mapped[str] = mapped_column(String, nullable=False, default="Easy")
    templates : Mapped[str] = mapped_column(String , nullable = False ) 
    def to_dict(self) : 
        return {
            "id": self.id,
            "title" :self.title ,
            "description": self.description ,
            "constraints" :self.constraints,
            "difficulty": self.difficulty ,
            "templates" :json.loads(self.templates)
        }

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()



