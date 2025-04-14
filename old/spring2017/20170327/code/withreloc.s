.data
string: .asciz "Hello, World!"
.text
main:
    movq $string, %rdi
    call puts
