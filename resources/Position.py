

class Position:
    def __init__(self, index: int, lineno: int, column: int, filename: str, file_text: str):
        self.index = index
        self.lineno = lineno
        self.column = column
        self.filename = filename
        self.file_text = file_text

    def advance(self, current_char: str | None = None):
        self.index += 1
        self.column += 1

        if current_char == "\n":
            self.lineno += 1
            self.column = 0

        return self

    def reverse(self, amount=1):
        self.index -= amount
        self.column -= amount

        return self

    def copy(self):
        return Position(self.index, self.lineno, self.column, self.filename, self.file_text)
