class SpreadSheet:

    def __init__(self):
        self._cells = {}
        self._evaluating = set()

    def set(self, cell: str, value: str) -> None:
        self._cells[cell] = value

    def get(self, cell: str) -> str:
        return self._cells.get(cell, '')

    def evaluate(self, cell: str) -> int | str:
        if cell in self._evaluating:
            return "#Circular"

        self._evaluating.add(cell)
        value = self.get(cell)

        if value.isdigit():
            self._evaluating.remove(cell)
            return int(value)

        if value.startswith("'") and value.endswith("'"):
            self._evaluating.remove(cell)
            return value[1:-1]

        if value.startswith("="):
            formula_value = value[1:]

            if formula_value.isdigit():
                self._evaluating.remove(cell)
                return int(formula_value)

            elif formula_value.startswith("'") and formula_value.endswith("'"):
                self._evaluating.remove(cell)
                return formula_value[1:-1]

            if formula_value in self._cells:
                result = self.evaluate(formula_value)
                self._evaluating.remove(cell)
                return result

            try:
                return self._evaluate_expression(formula_value)
            except (ZeroDivisionError, ValueError):
                self._evaluating.remove(cell)
                return "#Error"

        self._evaluating.remove(cell)
        return "#Error"

    def _evaluate_expression(self, expression: str) -> int:
        # Replace cell references with their evaluated values
        for cell in self._cells:
            if cell in expression:
                expression = expression.replace(cell, str(self.evaluate(cell)))

        # Check for any non-numeric characters that are not operators
        if any(char not in '0123456789+-*/%() ' for char in expression):
            raise ValueError("Invalid characters in expression.")

        try:
            result = eval(expression)
            if isinstance(result, float) and not result.is_integer():
                raise ValueError()  # Raise an error if result is a float
            return int(result)
        except (ZeroDivisionError, TypeError, SyntaxError):
            raise ZeroDivisionError()
