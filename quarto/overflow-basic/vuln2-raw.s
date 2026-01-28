	.file	"vuln2-raw.c"
	.text
	.globl	vulnerable
	.type	vulnerable, @function
vulnerable:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	subq	$184, %rsp
	.cfi_def_cfa_offset 208
	movabsq	$-5915442685903131709, %rax
	movabsq	$-8557847242548099184, %rdx
	movq	%rax, 144(%rsp)
	movq	%rdx, 152(%rsp)
	movabsq	$5349494582043403636, %rax
	movabsq	$-953372589698228167, %rdx
	movq	%rax, 160(%rsp)
	movq	%rdx, 168(%rsp)
	movq	%rsp, %rbp
	movq	%rbp, %rdi
	call	gets@PLT
	leaq	112(%rsp), %rbx
	movq	%rbx, %rsi
	movq	%rbp, %rdi
	call	ComputeSHA256@PLT
	leaq	144(%rsp), %rdi
	movl	$32, %edx
	movq	%rbx, %rsi
	call	memcmp@PLT
	testl	%eax, %eax
	je	.L4
.L1:
	addq	$184, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
.L4:
	.cfi_restore_state
	call	Interesting@PLT
	jmp	.L1
	.cfi_endproc
.LFE0:
	.size	vulnerable, .-vulnerable
	.ident	"GCC: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
