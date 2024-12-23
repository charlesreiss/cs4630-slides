all: format bad ex-shellcodeloc stackloc.exe

info: info.c
	gcc -O3 -ggdb -z execstack -z relro -fcf-protection=none -o info info.c
info-nopie: info.c
	gcc -O3 -ggdb -no-pie -z execstack -z relro -fcf-protection=none -o info-nopie info.c
