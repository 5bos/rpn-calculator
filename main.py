from typing import Annotated
from urllib.parse import unquote
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import JSON, Column
from sqlmodel import Field, Session, SQLModel, create_engine, select

from utils.operand_utils import OPERANDS_MAPPING, OperandException
from db.stack import Stack, Item

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/rpn/op")
def get_operands(session: SessionDep):
    """Lists the available operands"""
    return {
        "success": True,
        "objects": [
            {"key": key, "symbol": value.symbol(), "description": value.description()}
            for key, value in OPERANDS_MAPPING.items()
        ],
    }


@app.post("/rpn/op/{op}/stack/{stack_id}")
def perform_operand(op: str, stack_id: int, session: SessionDep):
    """
    Applies the operand on the last two elements of the stack items, and replaces these
    items with the result of the operation
    """
    operator = OPERANDS_MAPPING.get(op)
    if not operator:
        raise HTTPException(
            status_code=404,
            detail=f'No operand found for "{op}". Supported operands are {list(OPERANDS_MAPPING.keys())}',
        )

    stack = session.get(Stack, stack_id)
    if not stack:
        raise HTTPException(status_code=404, detail=f"No stack found with id {stack_id}")

    if len(stack.items) < 2:
        raise HTTPException(status_code=400, detail=f"Stack must have at least 2 items")

    *remaining_items, y, x = stack.items

    try:
        result = operator.perform(x, y)
    except OperandException as e:
        raise HTTPException(status_code=400, detail=str(e))

    stack.sqlmodel_update({"items": [*remaining_items, result]})
    session.add(stack)
    session.commit()
    session.refresh(stack)
    return {"success": True, "object": stack}


@app.get("/rpn/stack/{stack_id}")
def get_stack(stack_id: int, session: SessionDep):
    """Return the stack with the given ID of 404"""
    stack = session.get(Stack, stack_id)
    if not stack:
        raise HTTPException(status_code=404, detail=f"No stack found with id {stack_id}")
    return {"success": True, "object": stack}


@app.post("/rpn/stack/", status_code=status.HTTP_201_CREATED)
def post_stack(stack: Stack, session: SessionDep):
    """Creates a stack with the items"""
    session.add(stack)
    session.commit()
    session.refresh(stack)

    return {"success": True, "object": stack}


@app.delete("/rpn/stack/{stack_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stack(stack_id: int, session: SessionDep):
    """Deletes a stack"""
    stack = session.get(Stack, stack_id)
    if stack:
        session.delete(stack)
        session.commit()

    return {"success": True}


@app.get("/rpn/stack/")
def list_stacks(session: SessionDep):
    """List all available stacks"""
    stacks = session.exec(select(Stack)).all()
    return {"success": True, "objects": stacks}


@app.post("/rpn/stack/{stack_id}")
def add_item_to_stack(stack_id: int, item: Item, session: SessionDep):
    """Add a single item to a stack"""
    stack = session.get(Stack, stack_id)
    if not stack:
        raise HTTPException(status_code=404, detail=f"No stack found with id {stack_id}")
    items = stack.items
    stack.sqlmodel_update({"items": [*items, item.value]})
    session.add(stack)
    session.commit()
    session.refresh(stack)
    return {"success": True, "object": stack}
