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
    parser.add_argument('-f', '--filename', required=False)
    parser.add_argument('-s', '--source_file', required=False, action='store')
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
            patcher.PatchCleaner(),
            patcher.NopSlideAdderFunctionPatcher()
            )
    patched = p.patch_code(code)
    save_to_file(filename, patched)


def clean_file(filename):
    code = get_code(filename)
    patch_free = patcher.PatchCleaner().wipe_existing_patches(code)
    save_to_file(filename, patch_free)


def read_files(source_file):
    f = open(source_file)
    lines = f.readlines()
    f.close()
    lines = map(lambda l: l.strip(), lines)
    lines = filter(lambda l: l and not l.startswith('#'), lines)
    return list(lines)


def run():
    args = parse_args()
    files = []
    if args.source_file:
        if args.filename:
            print("provider either a file or a sourcefile")
            exit(1)
        files = [args.filename]

    if args.source_file: 
        files = read_files(args.source_file)
        print(files)
        
    if args.operation == 'patch':
        for file in files:
            check_existence(file)
            check_format(file)
            print("patching ", file)
            patch_file(file)

    elif args.operation == 'clean':
        for file in files:
            check_existence(file)
            check_format(file)
            print("cleaning ", args.filename)
            clean_file(args.filename)
    else:
        raise Exception("Bad state")


if __name__ == '__main__':
    run()
