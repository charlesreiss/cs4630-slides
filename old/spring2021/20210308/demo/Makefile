all: format bad ex-shellcodeloc stackloc.exe

format: format.c
	gcc -Og -ggdb -D_FORITY_SOURCE=0 -no-pie -z execstack -z relro -fcf-protection=none -fno-stack-protector -o format format.c

bad: bad.c
	gcc -Og -ggdb -z execstack -z relro -fcf-protection=none -fno-stack-protector -o bad bad.c
bad-canary: bad.c
	gcc -Og -ggdb -fcf-protection=none -fstack-protector-all -o bad-canary bad.c
ex-shellcodeloc: ex-shellcodeloc.c
	gcc -Os -z execstack -z relro -fcf-protection=none -fno-stack-protector -o ex-shellcodeloc ex-shellcodeloc.c
stackloc.exe: stackloc.c
	gcc -Og -ggdb -z execstack -z relro -fcf-protection=none -fno-stack-protector -o stackloc.exe stackloc.c
