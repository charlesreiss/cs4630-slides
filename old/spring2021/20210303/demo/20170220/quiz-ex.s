	.file	"quiz-ex.c"
	.text
	.globl	giveQuiz
	.type	giveQuiz, @function
giveQuiz:
.LFB11:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	subq	$120, %rsp
	.cfi_def_cfa_offset 144
	movl	$0, 108(%rsp)
	movl	$questions, %ebx
	movl	$questions+160, %ebp
.L3:
	movq	%rsp, %rdi
	movl	$0, %eax
	call	gets
	movq	%rbx, %rsi
	movq	%rsp, %rdi
	call	checkAnswer
	testl	%eax, %eax
	je	.L2
	movl	108(%rsp), %eax
	addl	$1, %eax
	movl	%eax, 108(%rsp)
.L2:
	addq	$16, %rbx
	cmpq	%rbp, %rbx
	jne	.L3
	movl	108(%rsp), %eax
	addq	$120, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE11:
	.size	giveQuiz, .-giveQuiz
	.comm	questions,160,32
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
