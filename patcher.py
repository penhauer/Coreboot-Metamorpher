from abc import ABC, abstractmethod
import random
from typing_extensions import override
import function_finder
import typing
import re
import string
from patch_cleaner import PatchCleaner


class FunctionPatcher(ABC):
    
    @abstractmethod
    def patch_function(self, code: str) -> str:
        pass


SIGN_HEADER = "/* METAMORPHED SECTION START */"
SIGN_FOOTER = "/* METAMORPHED SECTION END */"
SIGN_HEADER_PATTERN = r"\/\* METAMORPHED SECTION START \*\/"
SIGN_FOOTER_PATTERN = r"\/\* METAMORPHED SECTION END \*\/"

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

def check_for_diff(s1, s2, code):
    get_end = lambda x: x.end
    ends_s1 = list(map(get_end, s1))
    ends_s2 = list(map(get_end, s2))

    for e2 in ends_s2:
        if e2 not in ends_s1:
            print("oh" * 10)
            pass
            # breakpoint()

class CodePatcher:

    def __init__(self, 
                 function_finder: function_finder.FunctionFinder,
                 patch_cleaner: PatchCleaner, 
                 patcher: FunctionPatcher) -> None:

        self.function_finder = function_finder
        self.patch_cleaner = patch_cleaner
        self.patcher = patcher

    def patch_code(self, code: str):
        patch_free = self.patch_cleaner.wipe_existing_patches(code)
        scopes = self.function_finder.get_function_scopes(patch_free)

        try:
            s2 = function_finder.RegexFunctionFinder().get_function_scopes(patch_free)
            check_for_diff(s2, scopes, patch_free)
        except Exception as e:
            import traceback
            traceback.print_exception(e)


        scope_patcher = ScopePatcher(self.patcher)
        patched = scope_patcher.patch_functions(code, scopes)
        return patched
