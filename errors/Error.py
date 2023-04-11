from resources import Position
from utils.string_with_arrows import string_with_arrows


class Error:
    def __init__(self, pos_start, pos_end, error_name: str, details: str):
        self.pos_start: Position = pos_start
        self.pos_end = pos_end
        self.error_name: str = error_name
        self.details: str = details

    def as_string(self) -> str:
        result = f"{self.error_name}: {self.details} | "
        result += f"File {self.pos_start.filename}, line {self.pos_start.lineno + 1}"
        result += f"\n\n {string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)}"
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Expected Character", details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)


class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details} | "
        result += f"\n\n {string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)}"
        return result

    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f"   File {pos.filename}, line {pos.lineno + 1}, in {ctx.display_name}\n" + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback (most recent call last):\n" + result
