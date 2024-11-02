class SpreadSheet:

    def __init__(self):
        self._cells = {}

    def set(self, cell: str, value: str) -> None:
        self._cells[cell] = value

    def get(self, cell: str) -> str:
        return self._cells.get(cell, '')

    def evaluate(self, cell: str) -> int | str:
        value = self.get(cell)

        if value.isdigit():
            return int(value)

        try:
            float(value)
            return "#Error"
        except ValueError:
            pass

        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]

        if value.startswith("="):
            formula_value = value[1:]
            if formula_value.isdigit():
                return int(formula_value)
            elif formula_value.startswith("'") and formula_value.endswith("'"):
                return formula_value[1:-1]
            try:
                float(formula_value)
                return "#Error"
            except ValueError:
                return "#Error"

        return "#Error"
