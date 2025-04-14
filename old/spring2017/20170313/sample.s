	.file	"sample.cc"
	.section	.text.unlikely._ZN7Polygon4drawEP6Canvas,"axG",@progbits,_ZN7Polygon4drawEP6Canvas,comdat
	.align 2
.LCOLDB0:
	.section	.text._ZN7Polygon4drawEP6Canvas,"axG",@progbits,_ZN7Polygon4drawEP6Canvas,comdat
.LHOTB0:
	.align 2
	.weak	_ZN7Polygon4drawEP6Canvas
	.type	_ZN7Polygon4drawEP6Canvas, @function
_ZN7Polygon4drawEP6Canvas:
.LFB0:
	.cfi_startproc
	ret
	.cfi_endproc
.LFE0:
	.size	_ZN7Polygon4drawEP6Canvas, .-_ZN7Polygon4drawEP6Canvas
	.section	.text.unlikely._ZN7Polygon4drawEP6Canvas,"axG",@progbits,_ZN7Polygon4drawEP6Canvas,comdat
.LCOLDE0:
	.section	.text._ZN7Polygon4drawEP6Canvas,"axG",@progbits,_ZN7Polygon4drawEP6Canvas,comdat
.LHOTE0:
	.section	.text.unlikely,"ax",@progbits
.LCOLDB1:
	.section	.text.startup,"ax",@progbits
.LHOTB1:
	.globl	main
	.type	main, @function
main:
.LFB1:
	.cfi_startproc
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$8, %edi
	call	_Znwm
	movq	$_ZTV7Polygon+16, (%rax)
	movq	%rax, %rdi
	call	_ZdlPv
	xorl	%eax, %eax
	popq	%rdx
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE1:
	.size	main, .-main
	.section	.text.unlikely
.LCOLDE1:
	.section	.text.startup
.LHOTE1:
	.weak	_ZTS5Shape
	.section	.rodata._ZTS5Shape,"aG",@progbits,_ZTS5Shape,comdat
	.type	_ZTS5Shape, @object
	.size	_ZTS5Shape, 7
_ZTS5Shape:
	.string	"5Shape"
	.weak	_ZTI5Shape
	.section	.rodata._ZTI5Shape,"aG",@progbits,_ZTI5Shape,comdat
	.align 8
	.type	_ZTI5Shape, @object
	.size	_ZTI5Shape, 16
_ZTI5Shape:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS5Shape
	.weak	_ZTS7Polygon
	.section	.rodata._ZTS7Polygon,"aG",@progbits,_ZTS7Polygon,comdat
	.align 8
	.type	_ZTS7Polygon, @object
	.size	_ZTS7Polygon, 9
_ZTS7Polygon:
	.string	"7Polygon"
	.weak	_ZTI7Polygon
	.section	.rodata._ZTI7Polygon,"aG",@progbits,_ZTI7Polygon,comdat
	.align 8
	.type	_ZTI7Polygon, @object
	.size	_ZTI7Polygon, 24
_ZTI7Polygon:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS7Polygon
	.quad	_ZTI5Shape
	.weak	_ZTV7Polygon
	.section	.rodata._ZTV7Polygon,"aG",@progbits,_ZTV7Polygon,comdat
	.align 8
	.type	_ZTV7Polygon, @object
	.size	_ZTV7Polygon, 24
_ZTV7Polygon:
	.quad	0
	.quad	_ZTI7Polygon
	.quad	_ZN7Polygon4drawEP6Canvas
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
