from abc import ABC, abstractmethod
import random
from typing_extensions import override
import function_finder
import typing
import re
import string
import traceback



class FunctionPatcher(ABC):
    
    @abstractmethod
    def patch_function(self, code: str) -> str:
        pass


SIGN_HEADER = "/* METAMORPHED SECTION START */"
SIGN_FOOTER = "/* METAMORPHED SECTION END */"
SIGN_HEADER_PATTERN = r"\/\* METAMORPHED SECTION START \*\/"
SIGN_FOOTER_PATTERN = r"\/\* METAMORPHED SECTION END \*\/"
ANYTHING_WITH_NO_COMMENT = r"(?:[^\/]|\/[^*])*"

class PatchCleaner:
    def __init__(self) -> None:
        pass

    def wipe_existing_patches(self, code: str) -> str:
        p = rf"\n\s*{SIGN_HEADER_PATTERN}{ANYTHING_WITH_NO_COMMENT}{SIGN_FOOTER_PATTERN}\n"
        return re.sub(p, "", code, flags=re.MULTILINE + re.DOTALL)


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
        m = re.match(function_finder.RegexFunctionFinder.FUNCTION_REGEX, func_code)
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


class ScopePatcher:
    def __init__(self, function_patcher: FunctionPatcher) -> None:
        self.function_patcher = function_patcher

    def patch_functions(self, code: str, scopes: typing.List[function_finder.Scope]) -> str:
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


class CodePatcher:

    def __init__(self, 
                 function_finder: function_finder.FunctionFinder,
                 patch_cleaner: PatchCleaner, 
                 patcher: FunctionPatcher) -> None:

        self.function_finder = function_finder
        self.patch_cleaner = patch_cleaner
        self.patcher = patcher

    def patch_code(self, code: str):
        scopes = self.function_finder.get_function_scopes(code)
        scope_patcher = ScopePatcher(self.patcher)
        patched = scope_patcher.patch_functions(code, scopes)
        return patched


"""
compares two fucntion finders in terms of functions found on some code
"""
class FunctionFinderComparer:
    def __init__(self, a: function_finder.FunctionFinder, b: function_finder.FunctionFinder) -> None:
        self.a = a
        self.b = b

    """ 
    only looks for differences in scopes's ends (and excludes beginnings) because two different 
    function scope finders usually find the end of functions equally and beginnings might differ.
    """
    def compare(self, code: str) -> None:
        try:
            scopes1 = self.a.get_function_scopes(code)
            scopes2 = self.b.get_function_scopes(code)

            get_end = lambda x: x.end
            ends_s1 = set(map(get_end, scopes1))
            ends_s2 = set(map(get_end, scopes2))

            def get_scope_by_end(scopes: typing.List[function_finder.Scope], end: int):
                for scope in scopes:
                    if scope.end == end:
                        return scope
                return None

            da = ends_s1 - ends_s2
            db = ends_s2 - ends_s1


            if len(da) >= 1:
                la = map(lambda x: get_scope_by_end(scopes1, x), da)
                print(f"warning, found functions {la} in {self.a} not in {self.b}")

            if len(db) >= 1:
                lb = map(lambda x: get_scope_by_end(scopes2, x), db)
                print(f"warning, found functions {lb} in {self.b} not in {self.a}")

        except Exception as e:
            print("error while finding function scopes")
            traceback.print_exception(e)


