	.file	"asan-check.cc"
	.bss
	.align 32
	.type	_ZStL8__ioinit, @object
	.size	_ZStL8__ioinit, 1
_ZStL8__ioinit:
	.zero	64
	.text
	.globl	_Z17do_something_withPl
	.type	_Z17do_something_withPl, @function
_Z17do_something_withPl:
.LASANPC1021:
.LFB1021:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1021:
	.size	_Z17do_something_withPl, .-_Z17do_something_withPl
	.globl	__asan_stack_malloc_2
	.section	.rodata
.LC0:
	.string	"1 32 80 5 array "
	.text
	.globl	_Z10vulnerableli
	.type	_Z10vulnerableli, @function
_Z10vulnerableli:
.LASANPC1022:
.LFB1022:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$184, %rsp
	.cfi_offset 13, -24
	.cfi_offset 12, -32
	.cfi_offset 3, -40
	movq	%rdi, -200(%rbp)
	movl	%esi, -204(%rbp)
	leaq	-192(%rbp), %rbx
	movq	%rbx, %r13
	cmpl	$0, __asan_option_detect_stack_use_after_return(%rip)
	je	.L2
	movq	%rbx, %rsi
	movl	$160, %edi
	call	__asan_stack_malloc_2
	movq	%rax, %rbx
.L2:
	leaq	160(%rbx), %rax
	movq	$1102416563, (%rbx)
	movq	$.LC0, 8(%rbx)
	movq	$.LASANPC1022, 16(%rbx)
	movq	%rbx, %r12
	shrq	$3, %r12
	movl	$-235802127, 2147450880(%r12)
	movl	$-185335808, 2147450892(%r12)
	movl	$-202116109, 2147450896(%r12)
	movq	%fs:40, %rsi
	movq	%rsi, -40(%rbp)
	xorl	%esi, %esi
	movq	$1, -128(%rax)
	movq	$2, -120(%rax)
	movq	$3, -112(%rax)
	movq	$4, -104(%rax)
	movq	$5, -96(%rax)
	movq	$6, -88(%rax)
	movq	$7, -80(%rax)
	movq	$8, -72(%rax)
	movq	$9, -64(%rax)
	movq	$10, -56(%rax)
	leaq	-128(%rax), %rdx
	movl	-204(%rbp), %ecx
	movslq	%ecx, %rcx
	salq	$3, %rcx
	addq	%rcx, %rdx
	movq	%rdx, %rcx
	shrq	$3, %rcx
	addq	$2147450880, %rcx
	movzbl	(%rcx), %ecx
	testb	%cl, %cl
	je	.L6
	movq	%rdx, %rdi
	call	__asan_report_store8
.L6:
	movl	-204(%rbp), %edx
	movslq	%edx, %rdx
	movq	$0, -128(%rax,%rdx,8)
	addq	$-128, %rax
	movq	%rax, %rdi
	call	_Z17do_something_withPl
	nop
	cmpq	%rbx, %r13
	je	.L3
	movq	$1172321806, (%rbx)
	movabsq	$-723401728380766731, %rax
	movq	%rax, 2147450880(%r12)
	movabsq	$-723401728380766731, %rax
	movq	%rax, 2147450888(%r12)
	movl	$-168430091, 2147450896(%r12)
	jmp	.L4
.L3:
	movl	$0, 2147450880(%r12)
	movq	$0, 2147450892(%r12)
.L4:
	movq	-40(%rbp), %rax
	xorq	%fs:40, %rax
	je	.L7
	call	__stack_chk_fail
.L7:
	addq	$184, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1022:
	.size	_Z10vulnerableli, .-_Z10vulnerableli
	.section	.rodata
.LC1:
	.string	"2 32 4 6 offset 96 8 5 value "
	.text
	.globl	main
	.type	main, @function
main:
.LASANPC1023:
.LFB1023:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$160, %rsp
	.cfi_offset 14, -24
	.cfi_offset 13, -32
	.cfi_offset 12, -40
	.cfi_offset 3, -48
	leaq	-192(%rbp), %r12
	movq	%r12, %r14
	cmpl	$0, __asan_option_detect_stack_use_after_return(%rip)
	je	.L8
	movq	%r12, %rsi
	movl	$160, %edi
	call	__asan_stack_malloc_2
	movq	%rax, %r12
.L8:
	leaq	160(%r12), %rax
	movq	%rax, %r13
	movq	$1102416563, (%r12)
	movq	$.LC1, 8(%r12)
	movq	$.LASANPC1023, 16(%r12)
	movq	%r12, %rbx
	shrq	$3, %rbx
	movl	$-235802127, 2147450880(%rbx)
	movl	$-185273340, 2147450884(%rbx)
	movl	$-218959118, 2147450888(%rbx)
	movl	$-185273344, 2147450892(%rbx)
	movl	$-202116109, 2147450896(%rbx)
	movq	%fs:40, %rax
	movq	%rax, -40(%rbp)
	xorl	%eax, %eax
	leaq	-64(%r13), %rax
	movq	%rax, %rsi
	movl	$_ZSt3cin, %edi
	call	_ZNSirsERl
	movq	%rax, %rdx
	leaq	-128(%r13), %rax
	movq	%rax, %rsi
	movq	%rdx, %rdi
	call	_ZNSirsERi
	movl	-128(%r13), %edx
	movq	-64(%r13), %rax
	movl	%edx, %esi
	movq	%rax, %rdi
	call	_Z10vulnerableli
	movl	$0, %eax
	cmpq	%r12, %r14
	je	.L9
	movq	$1172321806, (%r12)
	movabsq	$-723401728380766731, %rcx
	movq	%rcx, 2147450880(%rbx)
	movabsq	$-723401728380766731, %rcx
	movq	%rcx, 2147450888(%rbx)
	movl	$-168430091, 2147450896(%rbx)
	jmp	.L10
.L9:
	movq	$0, 2147450880(%rbx)
	movq	$0, 2147450888(%rbx)
	movl	$0, 2147450896(%rbx)
.L10:
	movq	-40(%rbp), %rdx
	xorq	%fs:40, %rdx
	je	.L13
	call	__stack_chk_fail
.L13:
	addq	$160, %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1023:
	.size	main, .-main
	.section	.rodata
.LC2:
	.string	"asan-check.cc"
	.text
	.type	_Z41__static_initialization_and_destruction_0ii, @function
_Z41__static_initialization_and_destruction_0ii:
.LASANPC1025:
.LFB1025:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	cmpl	$1, -4(%rbp)
	jne	.L17
	movl	$.LC2, %edi
	call	__asan_before_dynamic_init
	cmpl	$65535, -8(%rbp)
	jne	.L16
	movl	$_ZStL8__ioinit, %edi
	call	_ZNSt8ios_base4InitC1Ev
	movl	$__dso_handle, %edx
	movl	$_ZStL8__ioinit, %esi
	movl	$_ZNSt8ios_base4InitD1Ev, %edi
	call	__cxa_atexit
.L16:
	call	__asan_after_dynamic_init
.L17:
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1025:
	.size	_Z41__static_initialization_and_destruction_0ii, .-_Z41__static_initialization_and_destruction_0ii
	.type	_GLOBAL__sub_I__Z17do_something_withPl, @function
_GLOBAL__sub_I__Z17do_something_withPl:
.LASANPC1026:
.LFB1026:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	$65535, %esi
	movl	$1, %edi
	call	_Z41__static_initialization_and_destruction_0ii
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1026:
	.size	_GLOBAL__sub_I__Z17do_something_withPl, .-_GLOBAL__sub_I__Z17do_something_withPl
	.section	.init_array,"aw"
	.align 8
	.quad	_GLOBAL__sub_I__Z17do_something_withPl
	.section	.rodata
.LC3:
	.string	"/usr/include/c++/5/iostream"
	.data
	.align 16
	.type	.LASANLOC1, @object
	.size	.LASANLOC1, 16
.LASANLOC1:
	.quad	.LC3
	.long	74
	.long	25
	.section	.rodata
.LC4:
	.string	"__ioinit"
	.data
	.align 32
	.type	.LASAN0, @object
	.size	.LASAN0, 56
.LASAN0:
	.quad	_ZStL8__ioinit
	.quad	1
	.quad	64
	.quad	.LC4
	.quad	.LC2
	.quad	1
	.quad	.LASANLOC1
	.text
	.type	_GLOBAL__sub_D_00099_0__Z17do_something_withPl, @function
_GLOBAL__sub_D_00099_0__Z17do_something_withPl:
.LFB1027:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	$1, %esi
	movl	$.LASAN0, %edi
	call	__asan_unregister_globals
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1027:
	.size	_GLOBAL__sub_D_00099_0__Z17do_something_withPl, .-_GLOBAL__sub_D_00099_0__Z17do_something_withPl
	.section	.fini_array.00099,"aw"
	.align 8
	.quad	_GLOBAL__sub_D_00099_0__Z17do_something_withPl
	.text
	.type	_GLOBAL__sub_I_00099_1__Z17do_something_withPl, @function
_GLOBAL__sub_I_00099_1__Z17do_something_withPl:
.LFB1028:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	call	__asan_init_v4
	movl	$1, %esi
	movl	$.LASAN0, %edi
	call	__asan_register_globals
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1028:
	.size	_GLOBAL__sub_I_00099_1__Z17do_something_withPl, .-_GLOBAL__sub_I_00099_1__Z17do_something_withPl
	.section	.init_array.00099,"aw"
	.align 8
	.quad	_GLOBAL__sub_I_00099_1__Z17do_something_withPl
	.hidden	__dso_handle
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
