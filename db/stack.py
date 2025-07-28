from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class Item(SQLModel):
    value: float = Field(default=0.0)


class Stack(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    items: list[Item] = Field(default_factory=list, sa_column=Column(JSON))
