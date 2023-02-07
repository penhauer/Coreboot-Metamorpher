# Coreboot-Metamorpher
Produces metamorphic versions of Coreboot by inserting junk instructions into source code

This project aims to produce metamorphic versions of Coreboot image by inserting asm instructions into C sourcecode. <a href="https://github.com/coreboot/coreboot">Coreboot</a> is a opensource firmware which can replace proprietary firmwares like BIOS and UEFI. Metamorphic clones of a program, are verions of it that have the same observable external behaviour but differ in the internal structure. The idea of producing metamorphic clones, is to increase software diversity analogous to diversity in viruses. Thus, if an attacker finds an exploit in one version, the same attack is not replayable on every other version. In other words, we aim to produce BOBE (**B**reak **O**nce **B**reak **E**verywhere) resitance to the different clones of the software.

# How it works

Using a C parser, functions of a C source code file are identified, and each one is "patched" with a probability of p. In the beginning of every patched function, some "Junk" statements are inserted which effectively do nothing and hence do not affect program's behaviour but change the address which every function resides in. In otherwords, 
<a href="https://tree-sitter.github.io/tree-sitter/">Tree-sitter</a>'s python binding <a href="https://github.com/tree-sitter/py-tree-sitter">py-tree-sitter</a> is used as the C parser. 


Here is an example of junk statements inserted:

```C
void sb_rtc_init(void)
{
    /* METAMORPHED SECTION START */
    __asm__ volatile (
        "nop\n\tnop\n\tnop\n\tpush %eax\n\tpop %eax\n\tnop\n\tnop"
    );
    /* METAMORPHED SECTION END */

	int rtc_failed = rtc_failure();

	if (rtc_failed) {
		if (CONFIG(ELOG))
			elog_add_event(ELOG_TYPE_RTC_RESET);
		pci_update_config8(PCH_LPC_DEV, D31F0_GEN_PMCON_3,
				   ~RTC_BATTERY_DEAD, 0);
	}

	printk(BIOS_DEBUG, "RTC: failed = 0x%x\n", rtc_failed);

	cmos_init(rtc_failed);
}

```

This is the equivalent function in assembly found by inspecting the corresponding objectfile by `objdump`. Notice how the nops and the push and pop on %x are in the beginning of the assembly function after the function's prologue.
```asm
00000000 <sb_rtc_init>:
   0:   55                      push   %ebp
   1:   57                      push   %edi
   2:   56                      push   %esi
   3:   53                      push   %ebx
   4:   83 ec 0c                sub    $0xc,%esp
   7:   90                      nop
   8:   90                      nop
   9:   90                      nop
   a:   50                      push   %eax
   b:   58                      pop    %eax
   c:   90                      nop
   d:   90                      nop
   e:   e8 fc ff ff ff          call   f <sb_rtc_init+0xf>
  13:   85 c0                   test   %eax,%eax
  15:   89 c3                   mov    %eax,%ebx
  17:   74 25                   je     3e <sb_rtc_init+0x3e>
  19:   bf a4 f8 00 80          mov    $0x8000f8a4,%edi
  1e:   bd f8 0c 00 00          mov    $0xcf8,%ebp
  23:   89 f8                   mov    %edi,%eax
  25:   89 ea                   mov    %ebp,%edx
  27:   ef                      out    %eax,(%dx)
  28:   be fc 0c 00 00          mov    $0xcfc,%esi
  2d:   89 f2                   mov    %esi,%edx
  2f:   ec                      in     (%dx),%al
  30:   88 c1                   mov    %al,%cl
  32:   89 ea                   mov    %ebp,%edx
  34:   89 f8                   mov    %edi,%eax
  36:   ef                      out    %eax,(%dx)
	...
```

In pictures above, a block of junk nop instructions plus a redundant consecutive push and pop on %eax register is inserted via `__asm__` assembler instruction. The keyword `voltaile` causes the compiler to not optimize out the nops. More information on extended asm and assembler instructions can be found <a href="https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html">here</a>.


# Usage

To execute the project, execute the following command:


```bash
$ COREBOOT_PATH=/path/to/coreboot/root ./generate_n_copies ${NUMBER_OF_COPIES_NEEDED}
```
Providing the number of copies in the command, the script produces n copies of metamorphed coreboot image under `./clones` directory. Please not that a list of files to be metamorphed is in `files.txt` under `resources` repository. The current `files.txt` is the list of files for building coreboot for the i386 architecture. See the section about `files.txt` for more information regarding this file. Also, a compile.sh


# files.txt

This file is a list of files to wich patches are applied. Note that some of the lines in this file are commented out with `#` character. This is becuase choosing to patch functions of some files causes link time errors which I could not find the cause to this so I decided to simply comment them out from list. 

## Gathering the list of files

To collect a list of files needed to patch, just cd to the root of the project and execute the following command.

```bash
$ make filelist | grep '.*\.c$'
```

Coreboot by default, defines the target `filelist` which list according to the Makefile is the "Files used in build". The command filters the files with a `.c` ending as header files and some other files are also listed.


# Compliation and building notes
As stated, there were link time errors with some files which I did not manage to resolve. You may notice the same errors when building for a different architecture (than the current list of files for `i386`). In such a case, just comment the problematic files and you are good to go.
