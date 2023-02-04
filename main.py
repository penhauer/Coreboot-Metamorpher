import sys
import argparse
import os
import re
import typing
import random
import string
import subprocess


def check_existence(filename: str):
    if not os.path.exists(filename):
        print("file not exists")
        sys.exit(1)


def check_format(filename: str):
    if not filename.endswith('.c'):
        print(f"{filename} not a C source code")
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('operation')
    return parser.parse_args()


def get_code(filename: str):
    f = open(file=filename, mode="r")
    lines = f.readlines()
    content = ''.join(lines)
    f.close()
    return content


def find_function_scope(code: str, start_ind: int) -> typing.Tuple[int, int]:
    ind = start_ind
    st = []
    while True:
        if code[ind] == '{':
            st.append('{')
        elif code[ind] == '}':
            st.pop()
            if len(st) == 0:
                break
        ind += 1

    return start_ind, ind + 1


FUNCTION_IDENTIFIER_KEY = 'function_identifier'
IDENTIFIER_REGEX = r'[a-zA-Z_][a-zA-Z0-9_]+'
RET_TYPE_REGEX = rf'(?:{IDENTIFIER_REGEX}|{IDENTIFIER_REGEX}\s*\*)'
FUNCTION_REGEX = fr'({RET_TYPE_REGEX})\s*(?P<{FUNCTION_IDENTIFIER_KEY}>{IDENTIFIER_REGEX})\([^()]*\)\s*{{'


def find_functions_scopes_by_regex(code: str) -> typing.List[typing.Tuple[int, int]]:
    matches = re.finditer(FUNCTION_REGEX, code)
    return list(map(lambda match: find_function_scope(code, match.start()), matches))


from tree_sitter import Node, Language, Parser
C_LANG = Language('./c.so', 'c')
parser = Parser()
parser.set_language(C_LANG)

def find_functions_scopes_by_parser(code: str) -> typing.List[typing.Tuple[int, int]]:
    tree = parser.parse(code.encode("ascii"))
    root = tree.root_node
    # map((node.start_point, node.end_point), filter(lambda node: node.type == 'function_definition', root.children))
    scopes = []
    for child in root.children:
      if child.type == 'function_definition':
        scopes.append((child.start_byte, child.end_byte))
    return scopes


def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


SIGN_HEADER = "/* METAMORPHED SECTION START */"
SIGN_FOOTER = "/* METAMORPHED SECTION END */"
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

NOP_SLIDE = """
    {SIGN_HEADER}
    __asm__ volatile (
        {nop_slide}
    );
    {SIGN_FOOTER}
"""


def add_junk(func_code: str):
    m = re.match(FUNCTION_REGEX, func_code)
    assert m is not None
    return_type = m.group(1)
    int_var = get_random_string(4)
    if return_type == "void":
        junk = VOID_TEMPLATE.format(
            SIGN_HEADER=SIGN_HEADER,
            int_var=int_var,
            SIGN_FOOTER=SIGN_FOOTER
        )
    else:
        type_var = get_random_string(4)
        junk = NON_VOID_TEMPLATE.format(
            SIGN_HEADER=SIGN_HEADER,
            int_var=int_var, return_type=return_type, type_var=type_var,
            SIGN_FOOTER=SIGN_FOOTER
        )

    ind = func_code.find('{')
    if ind == -1:
        raise Exception("not a valid function code")
    morphed_code = func_code[:ind + 1] + junk + func_code[ind + 1:]
    return morphed_code


def add_nop_slides(func_code: str):
    nop_count = random.randint(1, 4)
    nop_str = 'nop\\n\\t'
    nop_slide = f'"{nop_str * nop_count}"'
    patch = NOP_SLIDE.format(
        SIGN_HEADER=SIGN_HEADER,
        nop_slide=nop_slide,
        SIGN_FOOTER=SIGN_FOOTER
    )
    ind = func_code.find('{')
    if ind == -1:
        raise Exception("not a valid function code")
    morphed_code = func_code[:ind + 1] + patch + func_code[ind + 1:]
    return morphed_code


PATCH_FUNCTION = add_nop_slides


def patch_functions(code: str, scopes: typing.List[typing.Tuple[int, int]]):
    patched_code = ""
    ind = 0
    for scope in scopes:
        s, e = scope
        if ind <= s:
            patched_code += code[ind:s]
            patched_code += PATCH_FUNCTION(code[s:e])
            ind = e

    patched_code += code[ind:]
    return patched_code


SIGN_HEADER_PATTERN = r"\/\* METAMORPHED SECTION START \*\/"
SIGN_FOOTER_PATTERN = r"\/\* METAMORPHED SECTION END \*\/"
ANYTHING_WITH_NO_COMMENT = r"(?:[^\/]|\/[^*])*"


def wipe_existing_patches(code):
    p = rf"\n\s*{SIGN_HEADER_PATTERN}{ANYTHING_WITH_NO_COMMENT}{SIGN_FOOTER_PATTERN}\n"
    return re.sub(p, "", code, flags=re.MULTILINE + re.DOTALL)

SCOPE_FINDER_FUNC = find_functions_scopes_by_parser

def sub(code, p):
    print(code[p[0]:p[1]])

def check_for_diff(s1, s2, code):
    get_end = lambda x: x[1]
    ends_s1 = list(map(get_end, s1))
    ends_s2 = list(map(get_end, s2))

    for e2 in ends_s2:
        if e2 not in ends_s1:
            print("oh" * 10)
            pass
            # breakpoint()


def patch_code(code: str):
    cleaned = wipe_existing_patches(code)
    scopes = SCOPE_FINDER_FUNC(cleaned)

    try:
        s2 = find_functions_scopes_by_regex(cleaned)
        check_for_diff(s2, scopes, cleaned)
    except Exception as e:
        print(e)

    patched = patch_functions(cleaned, scopes)
    return patched


def save_to_file(filename, text):
    f = open(file=filename, mode="w")
    f.write(text)
    f.close()


def patch_file(filename):
    code = get_code(filename)
    patched = patch_code(code)
    save_to_file(filename, patched)


def remove_comments_from_file(pathname: str):
    # removes comments using gcc preprocessor
    sp = subprocess.run(["gcc", "-fpreprocessed", "-dD", "-E", pathname], capture_output=True, text=True)
    return sp.stdout


def remove_comments(code):
    pathname = "/tmp/cleaned.c"
    save_to_file(pathname, code)
    return remove_comments_from_file(pathname)


def find_function_start_by_identifier(func_id, with_comments):
    print("\n"*20)
    print(func_id)
    start_ind = with_comments.find(func_id)
    assert start_ind != -1
    return find_function_scope(with_comments, start_ind)


def find_function_code_with_comments(comment_free, with_comments):
    matches = re.finditer(FUNCTION_REGEX, comment_free)
    for match in matches:
        func_id = match.groupdict()[FUNCTION_IDENTIFIER_KEY]
        scope = find_function_start_by_identifier(func_id, with_comments)
        print(with_comments[scope[0] : scope[1]])



def patch_by_removing_comments_first(filename: str):
    code = get_code(filename)
    patch_free = wipe_existing_patches(code)
    comment_free = remove_comments(patch_free)
    find_function_code_with_comments(comment_free, code)
    


def clean_file(filename):
    code = get_code(filename)
    patch_free = wipe_existing_patches(code)
    save_to_file(filename, patch_free)


def alter_patch(filename: str):
    code = get_code(filename)
    from pycparser import c_parser, c_ast, c_generator
    parser = c_parser.CParser()
    comment_free = remove_comments(code)
    print(comment_free)
    ast = parser.parse(comment_free)
    ast.show(offset=2)


# def dfs_on_node(node: tree_sitter.Node):
#   print(node.type)
#   for child in node.children:
#     if child.type == 'function_definition':
#       x = child.text.decode("ascii")
#       print(child.start_point, child.end_point)
# 
# 
# def parse_file(filename: str) -> None:
#     code = get_code(filename)
#     scopes = find_functions_scopes_by_regex(code)
#     for scope in scopes:
#       begin = scope[0]
#       end = scope[1]
#       print(code[begin:end])
#     return
#     C_LANG = tree_sitter.Language('./c.so', 'c')
#     parser = tree_sitter.Parser()
#     parser.set_language(C_LANG)
#     tree = parser.parse(code.encode("ascii"))
#     root = tree.root_node
#     dfs_on_node(root)


def run():
    args = parse_args()
    check_existence(args.filename)
    check_format(args.filename)
    if args.operation == 'patch':
        print("patching ", args.filename)
        patch_file(args.filename)
        # patch_by_removing_comments_first(args.filename)
        # alter_patch(args.filename)
    elif args.operation == 'clean':
        clean_file(args.filename)
    elif args.operation == 'parse':
        # parse_file(args.filename)
        pass
    else:
        raise Exception("Bad state")


if __name__ == '__main__':
    run()
