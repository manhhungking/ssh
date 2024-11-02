class SpreadSheet:
    def __init__(self):
        self._cells = {}

    def set(self, cell: str, value: str) -> None:
        self._cells[cell] = value

    def get(self, cell: str) -> str:
        return self._cells.get(cell, '')

    def evaluate(self, cell: str) -> int | str:
        value = self.get(cell)
        try:
            # Attempt to convert the value to an integer
            return int(value)
        except ValueError:
            # If it’s not an integer, return "#Error"
            return "#Error"
