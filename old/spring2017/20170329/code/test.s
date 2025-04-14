	.file	"test.cc"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.globl	_Z10vulnerablev
	.type	_Z10vulnerablev, @function
_Z10vulnerablev:
.LFB46:
	.cfi_startproc
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	addq	$-128, %rsp
	.cfi_def_cfa_offset 144
	leaq	8(%rsp), %rbx
	movq	%fs:40, %rax
	movq	%rax, 120(%rsp)
	xorl	%eax, %eax
	movq	%rbx, %rdi
	call	_ZN12FooAndBufferC1Ev
	movq	%rbx, %rdi
	call	gets
	movq	112(%rsp), %r8
	xorl	%eax, %eax
	orq	$-1, %rcx
	movq	%rbx, %rdi
	movq	%rbx, %rdx
	repnz scasb
	movq	(%r8), %rax
	movq	%r8, %rdi
	notq	%rcx
	leaq	-1(%rcx), %rsi
	call	*(%rax)
	movq	120(%rsp), %rax
	xorq	%fs:40, %rax
	je	.L2
	call	__stack_chk_fail
.L2:
	subq	$-128, %rsp
	.cfi_def_cfa_offset 16
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE46:
	.size	_Z10vulnerablev, .-_Z10vulnerablev
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
