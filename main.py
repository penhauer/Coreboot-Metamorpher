import sys
import argparse
import os
import re
import typing
import scope_finder
import patcher as patcher


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


def convert_scopes_to_scopes(scopes: typing.List[scope_finder.Scope]) -> typing.List[typing.Tuple[int, int]]:
    f: typing.Callable[[scope_finder.Scope], typing.Tuple[int, int]]
    f = lambda x: (x.begin, x.end)
    return list(map(f, scopes))


SIGN_HEADER_PATTERN = r"\/\* METAMORPHED SECTION START \*\/"
SIGN_FOOTER_PATTERN = r"\/\* METAMORPHED SECTION END \*\/"
ANYTHING_WITH_NO_COMMENT = r"(?:[^\/]|\/[^*])*"


def wipe_existing_patches(code):
    p = rf"\n\s*{SIGN_HEADER_PATTERN}{ANYTHING_WITH_NO_COMMENT}{SIGN_FOOTER_PATTERN}\n"
    return re.sub(p, "", code, flags=re.MULTILINE + re.DOTALL)

# scope_finder_class = parser.TreeSitterParserFunctionFinder
scope_finder_class = scope_finder.RegexFunctionFinder


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
    scopes = scope_finder_class(cleaned).get_function_scopes()

    try:
        s2 = scope_finder.RegexFunctionFinder(cleaned).get_function_scopes()
        s2 = convert_scopes_to_scopes(s2)
        check_for_diff(s2, convert_scopes_to_scopes(scopes), cleaned)
    except Exception as e:
        import traceback
        traceback.print_exception(e)


    patched = patcher.CodePatcher(patcher.NopSlideAdderFunctionPatcher()).patch_functions(code, scopes)
    return patched


def save_to_file(filename, text):
    f = open(file=filename, mode="w")
    f.write(text)
    f.close()


def patch_file(filename):
    code = get_code(filename)
    patched = patch_code(code)
    save_to_file(filename, patched)


def clean_file(filename):
    code = get_code(filename)
    patch_free = wipe_existing_patches(code)
    save_to_file(filename, patch_free)



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
        print("cleaning ", args.filename)
        clean_file(args.filename)
    else:
        raise Exception("Bad state")


if __name__ == '__main__':
    run()
