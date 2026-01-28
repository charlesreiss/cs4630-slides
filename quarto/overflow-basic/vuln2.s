vulnerable:
  endbr64
  pushq %rbp
  pushq %rbx
  subq  $184, %rsp
    ...
  movq  %rsp, %rbp
  movq  %rbp, %rdi
  call  gets@PLT
  leaq  112(%rsp), %rbx
  movq  %rbx, %rsi
  movq  %rbp, %rdi
  call  ComputeSHA256@PLT
  leaq  144(%rsp), %rdi
  movl  $32, %edx
  movq  %rbx, %rsi
  call  memcmp@PLT
  testl %eax, %eax
  je  .L4
.L1:
  addq  $184, %rsp
  popq  %rbx
  popq  %rbp
  ret
.L4:
  call  Interesting@PLT
  jmp .L1
