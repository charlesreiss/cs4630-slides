shellcode:    
    jmp afterString
string:
    .ascii "You have been infected with a virus!\n"
afterString:
    leaq string(%rip), %rsi
    xor %eax, %eax
    xor %edi, %edi
    movb $1, %al
    movb $37, %dl
    syscall
    movb $231, %al
    xor %edi, %edi
    syscall

