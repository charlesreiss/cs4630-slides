	.file	"example.cc"
	.text
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"Foo::bar"
	.text
	.align 2
	.globl	_ZN3Foo3barEv
	.type	_ZN3Foo3barEv, @function
_ZN3Foo3barEv:
.LFB0:
	.cfi_startproc
	endbr64
	leaq	.LC0(%rip), %rax
	ret
	.cfi_endproc
.LFE0:
	.size	_ZN3Foo3barEv, .-_ZN3Foo3barEv
	.section	.rodata.str1.1
.LC1:
	.string	"Baz::bar"
	.text
	.align 2
	.globl	_ZN3Baz3barEv
	.type	_ZN3Baz3barEv, @function
_ZN3Baz3barEv:
.LFB1:
	.cfi_startproc
	endbr64
	leaq	.LC1(%rip), %rax
	ret
	.cfi_endproc
.LFE1:
	.size	_ZN3Baz3barEv, .-_ZN3Baz3barEv
	.weak	_ZTS3Foo
	.section	.rodata._ZTS3Foo,"aG",@progbits,_ZTS3Foo,comdat
	.type	_ZTS3Foo, @object
	.size	_ZTS3Foo, 5
_ZTS3Foo:
	.string	"3Foo"
	.weak	_ZTI3Foo
	.section	.data.rel.ro._ZTI3Foo,"awG",@progbits,_ZTI3Foo,comdat
	.align 8
	.type	_ZTI3Foo, @object
	.size	_ZTI3Foo, 16
_ZTI3Foo:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS3Foo
	.weak	_ZTS3Baz
	.section	.rodata._ZTS3Baz,"aG",@progbits,_ZTS3Baz,comdat
	.type	_ZTS3Baz, @object
	.size	_ZTS3Baz, 5
_ZTS3Baz:
	.string	"3Baz"
	.weak	_ZTI3Baz
	.section	.data.rel.ro._ZTI3Baz,"awG",@progbits,_ZTI3Baz,comdat
	.align 8
	.type	_ZTI3Baz, @object
	.size	_ZTI3Baz, 24
_ZTI3Baz:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS3Baz
	.quad	_ZTI3Foo
	.weak	_ZTV3Foo
	.section	.data.rel.ro._ZTV3Foo,"awG",@progbits,_ZTV3Foo,comdat
	.align 8
	.type	_ZTV3Foo, @object
	.size	_ZTV3Foo, 24
_ZTV3Foo:
	.quad	0
	.quad	_ZTI3Foo
	.quad	_ZN3Foo3barEv
	.weak	_ZTV3Baz
	.section	.data.rel.ro._ZTV3Baz,"awG",@progbits,_ZTV3Baz,comdat
	.align 8
	.type	_ZTV3Baz, @object
	.size	_ZTV3Baz, 24
_ZTV3Baz:
	.quad	0
	.quad	_ZTI3Baz
	.quad	_ZN3Baz3barEv
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
