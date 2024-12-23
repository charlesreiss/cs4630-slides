	.file	"over-saved.c"
	.text
	.globl	example
	.type	example, @function
example:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$88, %rsp
	.cfi_def_cfa_offset 144
	movq	%fs:40, %rax
	movq	%rax, 72(%rsp)
	xorl	%eax, %eax
	call	getValue@PLT
	movq	%rax, %rbx
	xorl	%eax, %eax
	call	getValue@PLT
	movq	%rax, %r15
	xorl	%eax, %eax
	call	getValue@PLT
	movq	%rax, %r14
	xorl	%eax, %eax
	call	getValue@PLT
	movq	%rax, %r13
	xorl	%eax, %eax
	call	getValue@PLT
	movq	%rax, %r12
	xorl	%eax, %eax
	call	getValue@PLT
	movq	%rax, %rbp
	xorl	%eax, %eax
	call	getValue@PLT
	movq	%rax, 8(%rsp)
	xorl	%eax, %eax
	call	getValue@PLT
	movq	%rax, 16(%rsp)
	xorl	%eax, %eax
	call	getValue@PLT
	leaq	62(%rsp), %rdi
	movq	%rax, 24(%rsp)
	call	getAnother@PLT
	movl	$4, (%rbx)
	xorl	%eax, %eax
	leaq	4(%rbx), %rdi
	movl	$8, (%r15)
	movl	$10, (%r14)
	movl	$12, 0(%r13)
	call	doSomething@PLT
	movq	8(%rsp), %rax
	leaq	44(%rsp), %rdi
	movl	$14, (%r12)
	movl	$16, 0(%rbp)
	movl	$18, (%rax)
	movq	16(%rsp), %rax
	movl	$20, (%rax)
	movq	24(%rsp), %rax
	movl	$22, (%rax)
	xorl	%eax, %eax
	call	doSomething@PLT
	xorl	%eax, %eax
	call	getAnotherValue@PLT
	movl	%eax, 4(%rbx)
	xorl	%eax, %eax
	call	getAnotherValue@PLT
	movl	%eax, 4(%r15)
	xorl	%eax, %eax
	call	getAnotherValue@PLT
	movl	%eax, 4(%r14)
	xorl	%eax, %eax
	call	getAnotherValue@PLT
	movl	%eax, 4(%r13)
	xorl	%eax, %eax
	call	getAnotherValue@PLT
	movl	%eax, 4(%r12)
	xorl	%eax, %eax
	call	getAnotherValue@PLT
	movl	%eax, 4(%rbp)
	xorl	%eax, %eax
	call	getAnotherValue@PLT
	movq	8(%rsp), %rdx
	movl	%eax, 4(%rdx)
	xorl	%eax, %eax
	call	getAnotherValue@PLT
	movq	16(%rsp), %rcx
	movl	%eax, 4(%rcx)
	xorl	%eax, %eax
	call	getAnotherValue@PLT
	movq	24(%rsp), %rsi
	movl	%eax, 4(%rsi)
	movq	72(%rsp), %rax
	xorq	%fs:40, %rax
	je	.L2
	call	__stack_chk_fail@PLT
.L2:
	addq	$88, %rsp
	.cfi_def_cfa_offset 56
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE0:
	.size	example, .-example
	.ident	"GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
