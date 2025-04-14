all: test-64-nopie.exe test-32-nopie.exe test-64-pie.exe test-32-pie.exe test-format.exe test-format2.exe

test2-64-pie.s: test2.c
	gcc -S -m64 -pie -fPIE -O1 -fno-inline-functions $^ -o $@

test2-64-nopie.s: test2.c
	gcc -S -m64 -fno-PIE -O1 -fno-inline-functions $^ -o $@

test-32-pie.exe: test.c test2.c
	gcc -m32 -pie -fPIE -o $@ -O1 -fno-inline-functions $^

test-64-pie.exe: test.c test2.c
	gcc -m64 -pie -fPIE -o $@ -O1 -fno-inline-functions $^

test-64-nopie.exe: test.c test2.c
	gcc -m64 -fno-PIE -o $@ -O1 -fno-inline-functions $^

test-32-nopie.exe: test.c test2.c
	gcc -m32 -fno-PIE -o $@ -O1 -fno-inline-functions $^	

test-format.exe: test-format.c
	gcc -Os test-format.c -o test-format.exe

test-format2.exe: test-format2.c
	gcc -frandom-seed=42 -U_FORTIFY_SOURCE -Os test-format2.c -o test-format2.exe

clean:
	rm -f *.exe

.PHONY: all clean
