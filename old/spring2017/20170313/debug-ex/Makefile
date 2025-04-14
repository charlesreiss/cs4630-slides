all: bad bad-stripped

bad: bad.c
	$(CC) -std=c99 -Os -U_FORTIFY_SOURCE -fno-stack-protector -z execstack -frandom-seed=42 -o $@ $<

bad-stripped: bad.c
	$(CC) -std=c99 -Os -s -U_FORTIFY_SOURCE -fno-stack-protector -z execstack -frandom-seed=42 -o $@ $<

.PHONY: bad bad-stripped
