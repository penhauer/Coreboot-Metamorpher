#!/usr/bin/bash

if [ $# -lt 1 ]; then
  echo "please enter number of clones wanted" >&2
  exit 1
fi

copies=$1
re='^[0-9]+$'
if ! [[ ${copies} =~ ${re} ]]; then
   echo "enter a number" >&2
   exit 1
fi

if ! [ -d "./clones" ]; then
  mkdir "clones"
fi

# files.txt contains the C files to be patched
source_file=files.txt

for i in $(seq ${copies}); do
  echo "generating clone ${i}"
  ./venv/bin/python3 main.py -s ${source_file} patch
  cd ..
  ./compile.sh
  cd -
  label=$(date +"%Y.%m.%d_%T")
  cp "../build/coreboot.rom" "./clones/coreboot.rom_${label}"
done
