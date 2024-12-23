    leaq string(%rip), %rsi
    movl $1, %eax
    movl $37, %edi
    syscall
    /* Linux system call:
       exit_group(0)
     */
    movl $231, %eax
    xor %edi, %edi
    syscall
string: 
    .asciz "You have been infected with a virus!\n"
