	.file	"memcpy_chk.c"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.globl	vulnerable
	.type	vulnerable, @function
vulnerable:
.LFB10:
	.cfi_startproc
	subq	$72, %rsp
	.cfi_def_cfa_offset 80
	movslq	len(%rip), %rdx
	movq	attacker_controlled(%rip), %rsi
	leaq	14(%rsp), %rdi
	movl	$42, %ecx
	movq	%fs:40, %rax
	movq	%rax, 56(%rsp)
	xorl	%eax, %eax
	call	__memcpy_chk
	movq	56(%rsp), %rcx
	xorq	%fs:40, %rcx
	je	.L2
	call	__stack_chk_fail
.L2:
	addq	$72, %rsp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE10:
	.size	vulnerable, .-vulnerable
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
