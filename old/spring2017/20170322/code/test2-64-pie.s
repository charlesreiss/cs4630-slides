	.file	"test2.c"
	.text
	.globl	foo
	.type	foo, @function
foo:
.LFB0:
	.cfi_startproc
	movl	$3, %eax
	cmpl	$5, %edi
	ja	.L3
	movl	%edi, %edi
	leaq	.L4(%rip), %rax
	movslq	(%rax,%rdi,4), %rdx
	addq	%rdx, %rax
	jmp	*%rax
	.section	.rodata
	.align 4
	.align 4
.L4:
	.long	.L6-.L4
	.long	.L5-.L4
	.long	.L6-.L4
	.long	.L5-.L4
	.long	.L6-.L4
	.long	.L5-.L4
	.text
.L5:
	movl	$2, %eax
	ret
.L6:
	movl	$1, %eax
.L3:
	rep ret
	.cfi_endproc
.LFE0:
	.size	foo, .-foo
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
