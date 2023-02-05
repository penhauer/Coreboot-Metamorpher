from abc import abstractmethod, ABC
import typing
import re
from typing_extensions import override
import tree_sitter

class Scope:
    def __init__(self, begin: int, end: int) -> None:
        self.begin = begin
        self.end = end


class FunctionFinder(ABC):

    @abstractmethod
    def get_function_scopes(self) -> typing.List[Scope]:
        pass


class RegexFunctionFinder(FunctionFinder):

    FUNCTION_IDENTIFIER_KEY = 'function_identifier'
    IDENTIFIER_REGEX = r'[a-zA-Z_][a-zA-Z0-9_]+'
    RET_TYPE_REGEX = rf'(?:{IDENTIFIER_REGEX}|{IDENTIFIER_REGEX}\s*\*)'
    FUNCTION_REGEX = fr'({RET_TYPE_REGEX})\s*(?P<{FUNCTION_IDENTIFIER_KEY}>{IDENTIFIER_REGEX})\([^()]*\)\s*{{'


    def __init__(self, code: str) -> None:
        self.code = code

    def __find_function_scope_by_start_ind(self, start_ind: int) -> Scope:
        ind = start_ind
        st = []
        while True:
            if self.code[ind] == '{':
                st.append('{')
            elif self.code[ind] == '}':
                st.pop()
                if len(st) == 0:
                    break
            ind += 1

        return Scope(start_ind, ind + 1)


    @override
    def get_function_scopes(self) -> typing.List[Scope]:
        matches = re.finditer(RegexFunctionFinder.FUNCTION_REGEX, self.code)
        return list(map(lambda match: self.__find_function_scope_by_start_ind( match.start()), matches))


class TreeSitterParserFunctionFinder(FunctionFinder):
    C_LANG = tree_sitter.Language('./c.so', 'c')

    def __init__(self, code: str) -> None:
        self.code = code
        self.parser = tree_sitter.Parser()
        self.parser.set_language(TreeSitterParserFunctionFinder.C_LANG)
        self.tree = self.parser.parse(self.code.encode("ascii"))

    @override 
    def get_function_scopes(self) -> typing.List[Scope]:
        root = self.tree.root_node
        scopes = []
        for child in root.children:
            if child.type == 'function_definition':
                scopes.append(Scope(child.start_byte, child.end_byte))
        return scopes
