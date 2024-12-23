	.file	"uninit.cc"
	.text
	.globl	_Z17do_something_withPi
	.type	_Z17do_something_withPi, @function
_Z17do_something_withPi:
.LFB1570:
	.cfi_startproc
	endbr64
	ret
	.cfi_endproc
.LFE1570:
	.size	_Z17do_something_withPi, .-_Z17do_something_withPi
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"set"
.LC1:
	.string	"get"
.LC2:
	.string	"exit"
	.text
	.globl	_Z10vulnerablev
	.type	_Z10vulnerablev, @function
_Z10vulnerablev:
.LFB1571:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA1571
	endbr64
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	subq	$56, %rsp
	.cfi_def_cfa_offset 80
	movq	%fs:40, %rax
	movq	%rax, 40(%rsp)
	xorl	%eax, %eax
	leaq	8(%rsp), %rbp
.L4:
	leaq	24(%rsp), %rax
	movq	%rbp, %rsi
	leaq	_ZSt3cin(%rip), %rdi
	movq	$0, 16(%rsp)
	movq	%rax, 8(%rsp)
	movb	$0, 24(%rsp)
.LEHB0:
	call	_ZStrsIcSt11char_traitsIcESaIcEERSt13basic_istreamIT_T0_ES7_RNSt7__cxx1112basic_stringIS4_S5_T1_EE@PLT
	leaq	.LC0(%rip), %rsi
	movq	%rbp, %rdi
	call	_ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE7compareEPKc@PLT
	testl	%eax, %eax
	jne	.L3
	leaq	4(%rsp), %rsi
	leaq	_ZSt3cin(%rip), %rdi
	call	_ZNSirsERi@PLT
.L6:
	movq	%rbp, %rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv@PLT
	jmp	.L4
.L3:
	leaq	.LC1(%rip), %rsi
	movq	%rbp, %rdi
	call	_ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE7compareEPKc@PLT
	testl	%eax, %eax
	jne	.L5
	movl	4(%rsp), %esi
	leaq	_ZSt4cout(%rip), %rdi
	call	_ZNSolsEi@PLT
.LEHE0:
	jmp	.L6
.L5:
	leaq	.LC2(%rip), %rsi
	movq	%rbp, %rdi
	call	_ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE7compareEPKc@PLT
	testl	%eax, %eax
	jne	.L6
	movq	%rbp, %rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv@PLT
	movq	40(%rsp), %rax
	xorq	%fs:40, %rax
	je	.L8
	call	__stack_chk_fail@PLT
.L9:
	endbr64
	movq	%rax, %r12
.L7:
	movq	%rbp, %rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv@PLT
	movq	%r12, %rdi
.LEHB1:
	call	_Unwind_Resume@PLT
.LEHE1:
.L8:
	addq	$56, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE1571:
	.globl	__gxx_personality_v0
	.section	.gcc_except_table,"a",@progbits
.LLSDA1571:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1571-.LLSDACSB1571
.LLSDACSB1571:
	.uleb128 .LEHB0-.LFB1571
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L9-.LFB1571
	.uleb128 0
	.uleb128 .LEHB1-.LFB1571
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE1571:
	.text
	.size	_Z10vulnerablev, .-_Z10vulnerablev
	.globl	_Z4leakv
	.type	_Z4leakv, @function
_Z4leakv:
.LFB1572:
	.cfi_startproc
	endbr64
	subq	$40, %rsp
	.cfi_def_cfa_offset 48
	movq	%fs:40, %rax
	movq	%rax, 24(%rsp)
	xorl	%eax, %eax
	leaq	12(%rsp), %rdi
	movl	$34567890, 20(%rsp)
	movabsq	$100746141636518222, %rax
	movq	%rax, 12(%rsp)
	call	_Z17do_something_withPi
	movq	24(%rsp), %rax
	xorq	%fs:40, %rax
	je	.L14
	call	__stack_chk_fail@PLT
.L14:
	addq	$40, %rsp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE1572:
	.size	_Z4leakv, .-_Z4leakv
	.section	.text.startup,"ax",@progbits
	.globl	main
	.type	main, @function
main:
.LFB1573:
	.cfi_startproc
	endbr64
	pushq	%rax
	.cfi_def_cfa_offset 16
	call	_Z4leakv
	call	_Z10vulnerablev
	xorl	%eax, %eax
	popq	%rdx
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE1573:
	.size	main, .-main
	.type	_GLOBAL__sub_I__Z17do_something_withPi, @function
_GLOBAL__sub_I__Z17do_something_withPi:
.LFB2058:
	.cfi_startproc
	endbr64
	pushq	%rax
	.cfi_def_cfa_offset 16
	leaq	_ZStL8__ioinit(%rip), %rdi
	call	_ZNSt8ios_base4InitC1Ev@PLT
	movq	_ZNSt8ios_base4InitD1Ev@GOTPCREL(%rip), %rdi
	popq	%rcx
	.cfi_def_cfa_offset 8
	leaq	__dso_handle(%rip), %rdx
	leaq	_ZStL8__ioinit(%rip), %rsi
	jmp	__cxa_atexit@PLT
	.cfi_endproc
.LFE2058:
	.size	_GLOBAL__sub_I__Z17do_something_withPi, .-_GLOBAL__sub_I__Z17do_something_withPi
	.section	.init_array,"aw"
	.align 8
	.quad	_GLOBAL__sub_I__Z17do_something_withPi
	.local	_ZStL8__ioinit
	.comm	_ZStL8__ioinit,1,1
	.hidden	DW.ref.__gxx_personality_v0
	.weak	DW.ref.__gxx_personality_v0
	.section	.data.rel.local.DW.ref.__gxx_personality_v0,"awG",@progbits,DW.ref.__gxx_personality_v0,comdat
	.align 8
	.type	DW.ref.__gxx_personality_v0, @object
	.size	DW.ref.__gxx_personality_v0, 8
DW.ref.__gxx_personality_v0:
	.quad	__gxx_personality_v0
	.hidden	__dso_handle
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
