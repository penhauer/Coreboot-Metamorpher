# Coreboot-Metamorpher
Produces metamorphic versions of Coreboot by inserting junk instructions into source code

This project aims to produce Metamorphic versions of Coreboot image by inserting asm instructions into C sourcecode. <a href="https://tree-sitter.github.io/tree-sitter/">Tree-sitter</a>'s python binding <a href="https://github.com/tree-sitter/py-tree-sitter">py-tree-sitter</a> is used as the C parser. Using parser, functions of a C source code are identified, and each one is "patched" with a probability of p. In the beginning of every patched function, "Junk" statements effectively do nothing and hence do not affect program's behaviour but change the address which every function resides in.


Here is an example of nop statements inserted:

<div>
![image](https://user-images.githubusercontent.com/45599206/217078235-a97090cf-0cb5-454e-a45d-48b718b65e94.png)

![image](https://user-images.githubusercontent.com/45599206/217076462-a951e5a5-a106-4753-b9d0-b37e37365ec8.png)
</div>


# Runing

