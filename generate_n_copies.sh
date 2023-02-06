#!/usr/bin/bash

if [ $# -lt 1 ]; then
  echo "ERROR: please enter number of clones wanted" >&2
  exit 1
fi

copies=$1
re='^[0-9]+$'
if ! [[ ${copies} =~ ${re} ]]; then
   echo "ERROR: please enter a number" >&2
   exit 1
fi

if ! [ -d "./clones" ]; then
  mkdir "clones"
fi

# check if COREBOOT_PATH is set
[ -z ${COREBOOT_PATH} ] && echo "ERROR: set the variable COREBOOT_PATH as the /path/to/coreboot" >&2 && exit 1

# append a / to the end
COREBOOT_PATH="${COREBOOT_PATH}/"

# files.txt contains the C files to be patched
source_file=resources/files.txt

# filter lines starting with '#'
# files in this variable are relative to coreboot root directory
relative_files=$(grep --invert-match -E '^#' ${source_file})

#convert paths to paths relative to this script
absolute_files=$(echo "${relative_files}" | awk "{ print \"${COREBOOT_PATH}\" \$1 }")

for i in $(seq ${copies}); do
  label=$(date +"%Y.%m.%d_%T")
  echo "generating clone #${i} with label ${label}"
  ./venv/bin/python3 ./src/main.py patch -f ${absolute_files}
  cd ${COREBOOT_PATH}
  ./compile.sh
  cd -
  cp "${COREBOOT_PATH}/build/coreboot.rom" "./clones/coreboot.rom_${label}"
done
