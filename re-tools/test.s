base:
    movq $function + 0x1234, %rax
    subq $0x1234, %rax
    call *%rax

function:
    ret

