# Coreboot-Metamorpher
Produces metamorphic versions of Coreboot by inserting junk instructions into source code

This project aims to produce Metamorphic versions of Coreboot image by inserting asm instructions into C sourcecode. <a href="https://tree-sitter.github.io/tree-sitter/">Tree-sitter</a>'s python binding <a href="https://github.com/tree-sitter/py-tree-sitter">py-tree-sitter</a> is used as the C parser. Using parser, functions of a C source code are identified, and each one is "patched" with a probability of p. In the beginning of every patched function, "Junk" statements effectively do nothing and hence do not affect program's behaviour but change the address which every function resides in.


Here is an example of nop statements inserted:

```C
void bootmem_add_range(uint64_t start, uint64_t size,
		       const enum bootmem_type tag)
{
    /* METAMORPHED SECTION START */
    __asm__ volatile (
        "nop\n\tnop\n\t"
    );
    /* METAMORPHED SECTION END */

	assert(tag > BM_MEM_FIRST && tag < BM_MEM_LAST);
	assert(bootmem_is_initialized());

	memranges_insert(&bootmem, start, size, tag);
	if (tag <= BM_MEM_OS_CUTOFF) {
		/* Can't change OS tables anymore after they are written out. */
		assert(!bootmem_memory_table_written());
		memranges_insert(&bootmem_os, start, size, tag);
	};
}

```

In pictures above, a block of junk nop instructions is inserted via `__asm__` assembler instruction. The keyword `voltaile` causes the compiler to not optimize out the nops. More information on extended asm and assembler instructions can be found <a href="https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html">here</a>.


# Usage

To execute the project, execute the following command:


```bash
$ COREBOOT_PATH=/path/to/coreboot/root ./generate_n_copies ${NUMBER_OF_COPIES_NEEDED}
```
Providing the number of copies in the command, the script produces n copies of metamorphed coreboot image under `./clones` directory. Please not that a list of files to be metamorphed is in `files.txt` under `resources` repository. The current `files.txt` is the list of files for building coreboot for the i386 architecture. See the section about `files.txt` for more information regarding this file. 


# files.txt

This file is a list of files to wich patches are applied. Note that some of the lines in this file are commented out with `#` character. This is becuase choosing to patch functions of some files causes link time errors which I could not find the cause to this so I decided to simply comment them out from list. 

## gathering 
