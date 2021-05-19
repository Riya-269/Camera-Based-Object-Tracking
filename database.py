import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Image(Base):

    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    filename = Column(String)


if __name__ == "__main__":
    engine = create_engine('sqlite:///db.sqlite3')
    Base.metadata.create_all(engine)
