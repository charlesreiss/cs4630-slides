leaq string(%rip), %rdi
pushq $0x4004e0
ret
string:
.asciz "You have been infected!\n"
