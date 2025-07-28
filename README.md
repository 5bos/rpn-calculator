# RPN Calculator

## Description

This project represents a simple implementation of an RPN Calculator.

Given an array of items (example `[..., w, x, y]`) and a mathematical operand `op` one of (`+`, `-`, `*`, `/`) the calculator will return the value of `z = y {op} x` and inserts it at the end of list replacing the two element `x` and `y` to obtain `[..., w, z]`

## Setup the project

### Install the dependancies

To setup the project, first create a virtual env and activate it

```shell
python3 -m venv env
source env/bin/activate
```

then install the dependancies

```shell
pip install -e .
```

### Run the server

You can run the server by typing

```shell
fastapi dev main.py
```

You can now access the sever on the address http://127.0.0.1:8000

You can also access the swagger on the adress http://127.0.0.1:8000/docs

## Run the tests

To run the test within the virtualenv, simply run the command

```shell
pytest .
``` 