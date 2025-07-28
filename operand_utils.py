class BaseOperand:
    @classmethod
    def symbol(cls):
        raise NotImplementedError

    @classmethod
    def description(cls) -> str:
        raise NotImplementedError

    @classmethod
    def perform(cls, x: float, y: float) -> float:
        raise NotImplementedError


class OperandException(Exception):
    pass


class Addition(BaseOperand):
    @classmethod
    def symbol(cls):
        return "+"

    @classmethod
    def description(cls) -> str:
        return "Addition"

    @classmethod
    def perform(cls, x: float, y: float) -> float:
        return x + y


class Substraction(BaseOperand):
    @classmethod
    def symbol(cls):
        return "-"

    @classmethod
    def description(cls) -> str:
        return "Substraction"

    @classmethod
    def perform(cls, x: float, y: float) -> float:
        return x - y


class Multiplication(BaseOperand):
    @classmethod
    def symbol(cls):
        return "*"

    @classmethod
    def description(cls) -> str:
        return "Multiplication"

    @classmethod
    def perform(cls, x: float, y: float) -> float:
        return x * y


class Division(BaseOperand):
    @classmethod
    def symbol(cls):
        return "/"

    @classmethod
    def description(cls) -> str:
        return "Division"

    @classmethod
    def perform(cls, x: float, y: float) -> float:
        try:
            return x / y
        except ZeroDivisionError:
            raise OperandException("The divider is 0")


OPERANDS_MAPPING: dict[str, BaseOperand] = {
    "add": Addition,
    "sub": Substraction,
    "mul": Multiplication,
    "div": Division,
}
