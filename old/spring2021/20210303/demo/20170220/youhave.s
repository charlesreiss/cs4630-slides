    leaq string(%rip), %rsi
    movl $1, %eax
    movl $37, %edi
    syscall
    movl $231, %eax
    xor %rdi, %rdi
    syscall
string:
    .asciz "You have been infected with a virus!\n"

