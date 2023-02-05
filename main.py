import sys
import argparse
import os
import function_finder
import patcher
import patch_cleaner



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


def save_to_file(filename, text):
    f = open(file=filename, mode="w")
    f.write(text)
    f.close()


def patch_file(filename):
    code = get_code(filename)
    p = patcher.CodePatcher(
            function_finder.RegexFunctionFinder(),
            patch_cleaner.PatchCleaner(),
            patcher.NopSlideAdderFunctionPatcher()
            )
    patched = p.patch_code(code)
    save_to_file(filename, patched)


def clean_file(filename):
    code = get_code(filename)
    patch_free = patch_cleaner.PatchCleaner().wipe_existing_patches(code)
    save_to_file(filename, patch_free)


def run():
    args = parse_args()
    check_existence(args.filename)
    check_format(args.filename)
    if args.operation == 'patch':
        print("patching ", args.filename)
        patch_file(args.filename)
    elif args.operation == 'clean':
        print("cleaning ", args.filename)
        clean_file(args.filename)
    else:
        raise Exception("Bad state")


if __name__ == '__main__':
    run()
