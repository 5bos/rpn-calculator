# ToDo

## Choices made

- **FastAPI framework :** For a simple app like the RPN Calculator, I choose to use FastAPI because it is easy to implement, practival for such need, and does not require a lot of setup
- **The use of an Sqlite database :** I used an sqlite database for this project because it is easier to setup than a PostgreSQL database (for example) that may need extra dependancies and configuration. Also the data expected in this database is not so big, so an SQLite DB should be enough
- **Name of the operands :** I choose to use verbose operands `add`, `sub`, `div`, `mul` instead of (`+`, `-`, `/`, `*`) because the caracter `/` is not supported as the path parameter of an url.

## Improvements

- **Logging :** Logging is very usefull for debug
- **Code Quality :** Add some linting and typing checks (ruff, mypy)
- **Git Best Practices :** Add a pre-commit hook and a CI that runs some usefull checks (such as tests, linting, typing, ...)
- **Better split of modules :** This project can be improved with a better architecture with splitting modules and fonctionalities. Here, the `main.py` file contains all the project's logic
- **Testing :** The tests implemented cover the nominal cases. Some edges cases can also be tested to ensure a better code coverage (division by zero, adding a NaN item to a stack, ...)
