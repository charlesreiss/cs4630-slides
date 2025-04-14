
CC = gcc
CFLAGS = -frandom-seed=42 -fno-stack-protector -fno-inline-functions -Os -U_FORTIFY_SOURCE

overflow.exe: overflow.c
	$(CC) $(CFLAGS) $^ -o $@

exploit.exe: exploit.c
	$(CC) $(CFLAGS) $^ -o $@
