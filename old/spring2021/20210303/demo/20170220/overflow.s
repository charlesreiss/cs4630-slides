	.file	"overflow.c"
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"%s"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4,,15
	.globl	vulnerable
	.type	vulnerable, @function
vulnerable:
.LFB23:
	.cfi_startproc
	subq	$120, %rsp
	.cfi_def_cfa_offset 128
	movl	$.LC0, %edi
	xorl	%eax, %eax
	movq	%rsp, %rsi
	call	__isoc99_scanf
	movq	%rsp, %rdi
	call	do_something_with
	addq	$120, %rsp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE23:
	.size	vulnerable, .-vulnerable
	.section	.text.unlikely
.LCOLDE1:
	.text
.LHOTE1:
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
