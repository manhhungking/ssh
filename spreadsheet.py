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

        # Handle direct integers
        if value.isdigit():
            self._evaluating.remove(cell)
            return int(value)

        # Handle quoted strings
        if value.startswith("'") and value.endswith("'"):
            self._evaluating.remove(cell)
            return value[1:-1]

        # Handle formulas
        if value.startswith("="):
            formula_value = value[1:]
            if formula_value.startswith("'") and formula_value.endswith("'"):
                self._evaluating.remove(cell)
                return formula_value[1:-1]
            result = self._evaluate_expression(formula_value)
            self._evaluating.remove(cell)
            return result

        self._evaluating.remove(cell)
        return "#Error"

    def _evaluate_expression(self, expression: str) -> int | str:
        tokens = expression.replace('+', ' + ').replace('-', ' - ').replace('*', ' * ').replace('/', ' / ').split()

        for i, token in enumerate(tokens):
            if token in self._cells:
                result = self.evaluate(token)
                if isinstance(result, str) and result.startswith("#"):
                    return result  # Propagate error directly if found
                tokens[i] = str(result)

        modified_expression = ' '.join(tokens)

        # Check for invalid characters
        if any(char not in '0123456789+-*/%() ' for char in modified_expression):
            return "#Error"

        try:
            result = eval(modified_expression)
            if isinstance(result, float) and not result.is_integer():
                return "#Error"  # Avoid float results
            return int(result)
        except (ZeroDivisionError, TypeError, SyntaxError):
            return "#Error"
