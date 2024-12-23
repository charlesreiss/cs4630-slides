	.file	"vulnerable.c"
	.text
	.p2align 4
	.globl	vulnerable
	.type	vulnerable, @function
vulnerable:
.LFB11:
	.cfi_startproc
	endbr64
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	pxor	%xmm1, %xmm1
	subq	$96, %rsp
	.cfi_def_cfa_offset 112
	movq	%fs:40, %rax
	movq	%rax, 88(%rsp)
	xorl	%eax, %eax
	cmpl	$63, %esi
	ja	.L1
	movl	%esi, %ebx
	movslq	%esi, %rsi
	movq	%rdi, %rcx
	movl	$1, %edx
	salq	$2, %rsi
	leaq	16(%rsp), %rdi
	movss	%xmm1, 12(%rsp)
	call	fread@PLT
	movaps	16(%rsp), %xmm4
	movss	12(%rsp), %xmm1
	movaps	%xmm4, %xmm3
	mulps	%xmm4, %xmm3
	movaps	%xmm3, %xmm2
	movaps	%xmm3, %xmm0
	addss	%xmm1, %xmm2
	shufps	$85, %xmm3, %xmm0
	addss	%xmm0, %xmm2
	movaps	%xmm3, %xmm0
	unpckhps	%xmm3, %xmm0
	shufps	$255, %xmm3, %xmm3
	addss	%xmm0, %xmm2
	movaps	%xmm4, %xmm0
	addss	%xmm1, %xmm0
	movaps	%xmm4, %xmm1
	shufps	$85, %xmm4, %xmm1
	addss	%xmm3, %xmm2
	addss	%xmm1, %xmm0
	movaps	%xmm4, %xmm1
	unpckhps	%xmm4, %xmm1
	shufps	$255, %xmm4, %xmm4
	addss	%xmm1, %xmm0
	movaps	32(%rsp), %xmm1
	movaps	%xmm1, %xmm3
	mulps	%xmm1, %xmm3
	addss	%xmm4, %xmm0
	addss	%xmm1, %xmm0
	addss	%xmm3, %xmm2
	movaps	%xmm3, %xmm4
	shufps	$85, %xmm3, %xmm4
	addss	%xmm4, %xmm2
	movaps	%xmm3, %xmm4
	unpckhps	%xmm3, %xmm4
	shufps	$255, %xmm3, %xmm3
	addss	%xmm4, %xmm2
	addss	%xmm3, %xmm2
	movaps	%xmm1, %xmm3
	shufps	$85, %xmm1, %xmm3
	addss	%xmm3, %xmm0
	movaps	%xmm1, %xmm3
	unpckhps	%xmm1, %xmm3
	shufps	$255, %xmm1, %xmm1
	addss	%xmm3, %xmm0
	addss	%xmm1, %xmm0
	movaps	48(%rsp), %xmm1
	movaps	%xmm1, %xmm3
	mulps	%xmm1, %xmm3
	addss	%xmm1, %xmm0
	addss	%xmm3, %xmm2
	movaps	%xmm3, %xmm4
	shufps	$85, %xmm3, %xmm4
	addss	%xmm4, %xmm2
	movaps	%xmm3, %xmm4
	unpckhps	%xmm3, %xmm4
	shufps	$255, %xmm3, %xmm3
	addss	%xmm4, %xmm2
	addss	%xmm3, %xmm2
	movaps	%xmm1, %xmm3
	shufps	$85, %xmm1, %xmm3
	addss	%xmm3, %xmm0
	movaps	%xmm1, %xmm3
	unpckhps	%xmm1, %xmm3
	shufps	$255, %xmm1, %xmm1
	addss	%xmm3, %xmm0
	movaps	64(%rsp), %xmm3
	movaps	%xmm3, %xmm4
	mulps	%xmm3, %xmm4
	addss	%xmm1, %xmm0
	addss	%xmm4, %xmm2
	movaps	%xmm4, %xmm5
	movaps	%xmm4, %xmm1
	shufps	$85, %xmm4, %xmm5
	unpckhps	%xmm4, %xmm1
	shufps	$255, %xmm4, %xmm4
	addss	%xmm2, %xmm5
	movaps	%xmm3, %xmm2
	addss	%xmm0, %xmm2
	movaps	%xmm3, %xmm0
	shufps	$85, %xmm3, %xmm0
	addss	%xmm0, %xmm2
	movaps	%xmm3, %xmm0
	unpckhps	%xmm3, %xmm0
	shufps	$255, %xmm3, %xmm3
	addss	%xmm0, %xmm2
	movaps	%xmm1, %xmm0
	pxor	%xmm1, %xmm1
	cvtsi2ssl	%ebx, %xmm1
	addss	%xmm5, %xmm0
	subl	$1, %ebx
	addss	%xmm3, %xmm2
	addss	%xmm4, %xmm0
	mulss	%xmm2, %xmm2
	divss	%xmm1, %xmm2
	pxor	%xmm1, %xmm1
	cvtsi2ssl	%ebx, %xmm1
	subss	%xmm2, %xmm0
	divss	%xmm1, %xmm0
	movaps	%xmm0, %xmm1
.L1:
	movq	88(%rsp), %rax
	xorq	%fs:40, %rax
	jne	.L7
	addq	$96, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 16
	movaps	%xmm1, %xmm0
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret
.L7:
	.cfi_restore_state
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE11:
	.size	vulnerable, .-vulnerable
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
