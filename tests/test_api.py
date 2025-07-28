from fastapi.testclient import TestClient
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel import Session
from db.stack import Stack
from utils.operand_utils import OPERANDS_MAPPING


class TestRpnCalculator:
    def test_create_stack(self, session: Session, client: TestClient):
        assert len(session.exec(select(Stack)).all()) == 0
        payload = {"items": [1, 2, 3]}

        response = client.post("/rpn/stack/", json=payload)
        assert response.status_code == 201

        data = response.json()
        assert "success" in data
        assert data["success"] is True
        assert data["object"]["items"] == [1, 2, 3]
        assert "id" in data["object"]

        assert data["object"]["id"] == 1
        assert data["object"]["items"] == [1, 2, 3]

        assert len(session.exec(select(Stack)).all()) == 1

    def test_list_stack(self, session: Session, client: TestClient):
        stack_1 = Stack(id=1, items=[10, 20, 30])
        stack_2 = Stack(id=2, items=[11, 21, 31])
        session.add(stack_1)
        session.add(stack_2)
        session.flush()
        response = client.get("/rpn/stack/")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] is True

        assert "objects" in data
        assert len(data["objects"]) == 2
        assert {"id": 1, "items": [10, 20, 30]} in data["objects"]
        assert {"id": 2, "items": [11, 21, 31]} in data["objects"]

    def test_get_stack(self, session: Session, client: TestClient):
        stack = Stack(id=1, items=[10, 20, 30])
        session.add(stack)
        session.flush()
        response = client.get("/rpn/stack/1")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] is True

        assert "object" in data
        assert data["object"] == {"id": 1, "items": [10, 20, 30]}

    def test_delete_stack(self, session: Session, client: TestClient):
        stack = Stack(id=1, items=[10, 20, 30])
        session.add(stack)
        session.flush()
        response = client.delete("/rpn/stack/1")
        assert response.status_code == 204

    def test_add_element_to_stack(self, session: Session, client: TestClient):
        stack = Stack(id=1, items=[10, 20, 30])
        session.add(stack)
        session.flush()

        response = client.post("/rpn/stack/1", json={"value": 40})
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] is True
        assert "object" in data
        assert data["object"] == {"id": 1, "items": [10, 20, 30, 40]}

        session.refresh(stack)
        assert stack.items == [10, 20, 30, 40]

    def test_list_operands(self, session: Session, client: TestClient):
        response = client.get("/rpn/op")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] is True
        assert "objects" in data

        assert {"key": "add", "symbol": "+", "description": "Addition"} in data["objects"]
        assert {"key": "sub", "symbol": "-", "description": "Substraction"} in data["objects"]
        assert {"key": "mul", "symbol": "*", "description": "Multiplication"} in data["objects"]
        assert {"key": "div", "symbol": "/", "description": "Division"} in data["objects"]

    def test_perform_addition(self, session: Session, client: TestClient):
        stack = Stack(id=1, items=[10, 20, 30])
        session.add(stack)
        session.flush()

        response = client.post("/rpn/op/add/stack/1")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] is True
        assert "object" in data
        assert data["object"] == {"id": 1, "items": [10, 50]}

    def test_perform_substraction(self, session: Session, client: TestClient):
        stack = Stack(id=1, items=[10, 20, 30])
        session.add(stack)
        session.flush()

        response = client.post("/rpn/op/sub/stack/1")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] is True
        assert "object" in data
        assert data["object"] == {"id": 1, "items": [10, 10]}

    def test_perform_multiplication(self, session: Session, client: TestClient):
        stack = Stack(id=1, items=[10, 20, 30])
        session.add(stack)
        session.flush()

        response = client.post("/rpn/op/mul/stack/1")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] is True
        assert "object" in data
        assert data["object"] == {"id": 1, "items": [10, 600]}

    def test_perform_division(self, session: Session, client: TestClient):
        stack = Stack(id=1, items=[10, 20, 30])
        session.add(stack)
        session.flush()

        response = client.post("/rpn/op/div/stack/1")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] is True
        assert "object" in data
        assert data["object"] == {"id": 1, "items": [10, 1.5]}

    def test_unkown_operand(self, session: Session, client: TestClient):
        stack = Stack(id=1, items=[10, 20, 30])
        session.add(stack)
        session.flush()

        response = client.post("/rpn/op/UNKOWN/stack/1")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert 'No operand found for "UNKOWN". Supported operands are ' in data["detail"]

    def test_less_than_two_items(self, session: Session, client: TestClient):
        stack = Stack(id=1, items=[10])
        session.add(stack)
        session.flush()

        response = client.post("/rpn/op/div/stack/1")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Stack must have at least 2 items"

    def test_no_stack_with_id(self, session: Session, client: TestClient):
        assert session.get(Stack, 1) is None

        response = client.get("/rpn/stack/1")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "No stack found with id 1"
