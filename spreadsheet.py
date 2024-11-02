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

        try:
            float(value)
            self._evaluating.remove(cell)
            return "#Error"
        except ValueError:
            pass

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
                float(formula_value)
                self._evaluating.remove(cell)
                return "#Error"
            except ValueError:
                self._evaluating.remove(cell)
                return "#Error"

        self._evaluating.remove(cell)
        return "#Error"
