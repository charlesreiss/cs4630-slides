.global get_foo_string
get_foo_string:
    leaq .Lstring(%rip), %rax
    jmp .Ldone
.Lstring:
    .asciz "foo"
.Ldone:
    ret
