import sys
import argparse
import os
import function_finder
import patcher



def check_existence(filename: str):
    if not os.path.exists(filename):
        print(f"pathname {filename} not exists")
        sys.exit(1)


def check_format(filename: str):
    if not filename.endswith('.c'):
        print(f"{filename} not a C source code")
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument
    parser.add_argument('operation', choices=["patch", "clean"], help="operation to apply to files")
    parser.add_argument('-f', '--filename', nargs='+', required=False)
    return parser.parse_args()


def get_code(filename: str):
    f = open(file=filename, mode="r")
    lines = f.readlines()
    content = ''.join(lines)
    f.close()
    return content


def save_to_file(filename, text):
    f = open(file=filename, mode="w")
    f.write(text)
    f.close()


def patch_file(filename):
    code = get_code(filename)

    patch_cleaner = patcher.PatchCleaner()
    patch_free = patch_cleaner.wipe_existing_patches(code)

    comparer = patcher.FunctionFinderComparer(
            function_finder.RegexFunctionFinder(),
            function_finder.TreeSitterParserFunctionFinder()
            )
    comparer.compare(code)

    p = patcher.CodePatcher(
            function_finder.TreeSitterParserFunctionFinder(),
            patch_cleaner,
            patcher.NopSlideAdderFunctionPatcher()
            )

    patched = p.patch_code(patch_free)
    save_to_file(filename, patched)


def clean_file(filename):
    code = get_code(filename)
    patch_free = patcher.PatchCleaner().wipe_existing_patches(code)
    save_to_file(filename, patch_free)


def run():
    args = parse_args()
    files = args.filename

    for file in files:
        check_existence(file)
        check_format(file)

    if args.operation == 'patch':
        for file in files:
            print("patching ", file)
            patch_file(file)

    elif args.operation == 'clean':
        for file in files:
            print("cleaning ", args.filename)
            clean_file(args.filename)
    else:
        raise Exception("Bad state")


if __name__ == '__main__':
    run()
