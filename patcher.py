from abc import ABC, abstractmethod
import random
from typing_extensions import override
import scope_finder
import typing
import re
import string


class FunctionPatcher(ABC):
    
    @abstractmethod
    def patch_function(self, code: str) -> str:
        pass


SIGN_HEADER = "/* METAMORPHED SECTION START */"
SIGN_FOOTER = "/* METAMORPHED SECTION END */"

class NopSlideAdderFunctionPatcher(FunctionPatcher):

    NOP_SLIDE = """
    {SIGN_HEADER}
    __asm__ volatile (
        {nop_slide}
    );
    {SIGN_FOOTER}
"""

    def __init__(self) -> None:
        pass

    @override
    def patch_function(self, code: str):
        nop_count = random.randint(1, 4)
        nop_str = 'nop\\n\\t'
        nop_slide = f'"{nop_str * nop_count}"'
        patch = NopSlideAdderFunctionPatcher.NOP_SLIDE.format(
            SIGN_HEADER=SIGN_HEADER,
            nop_slide=nop_slide,
            SIGN_FOOTER=SIGN_FOOTER
        )
        ind = code.find('{')
        if ind == -1:
            raise Exception("not a valid function code")
        morphed_code = code[:ind + 1] + patch + code[ind + 1:]
        return morphed_code


class JunkReturnAdderFunctionPatcher(FunctionPatcher):

    VOID_TEMPLATE = """
    {SIGN_HEADER}
    int {int_var} = 0;
    if (({int_var} * {int_var} + {int_var}) % 2 == 1) {{
        return;
    }}
    {SIGN_FOOTER}
"""

    NON_VOID_TEMPLATE = """
    {SIGN_HEADER}
    int {int_var} = 0;
    if (({int_var} * {int_var} + {int_var}) % 2 == 1) {{
        {return_type} {type_var};
        return {type_var};
    }}
    {SIGN_FOOTER}
"""

    def __init__(self) -> None:
        pass


    @staticmethod
    def get_random_string(length):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))


    @override
    def patch_function(self, func_code: str) -> str:
        m = re.match(scope_finder.RegexFunctionFinder.FUNCTION_REGEX, func_code)
        assert m is not None
        return_type = m.group(1)
        int_var = self.get_random_string(4)
        if return_type == "void":
            junk = JunkReturnAdderFunctionPatcher.VOID_TEMPLATE.format(
                SIGN_HEADER=SIGN_HEADER,
                int_var=int_var,
                SIGN_FOOTER=SIGN_FOOTER
            )
        else:
            type_var = self.get_random_string(4)
            junk = JunkReturnAdderFunctionPatcher.NON_VOID_TEMPLATE.format(
                SIGN_HEADER=SIGN_HEADER,
                int_var=int_var, return_type=return_type, type_var=type_var,
                SIGN_FOOTER=SIGN_FOOTER
            )

        ind = func_code.find('{')
        if ind == -1:
            raise Exception("not a valid function code")
        morphed_code = func_code[:ind + 1] + junk + func_code[ind + 1:]
        return morphed_code


class CodePatcher:
    def __init__(self, function_patcher: FunctionPatcher) -> None:
        self.function_patcher = function_patcher

    def patch_functions(self, code: str, scopes: typing.List[scope_finder.Scope]):
        patched_code = ""
        ind = 0
        for scope in scopes:
            s, e = scope.begin, scope.end
            if ind <= s:
                patched_code += code[ind:s]
                patched_code += self.function_patcher.patch_function(code[s:e])
                ind = e

        patched_code += code[ind:]
        return patched_code

