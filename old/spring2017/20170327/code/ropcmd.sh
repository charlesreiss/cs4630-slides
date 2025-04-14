ldd ./overflow.exe
OFFSET=0x2aaaaacd3000
./ROPgadget-5.4/ROPgadget.py --offset $OFFSET --binary /lib/x86_64-linux-gnu/libc.so.6 >gadgets.txt 
./ROPgadget-5.4/ROPgadget.py --offset $OFFSET --binary /lib/x86_64-linux-gnu/libc.so.6 >gadgets-nonewline.txt
./ROPgadget-5.4/ROPgadget.py --offset $OFFSET --binary /lib/x86_64-linux-gnu/libc.so.6 --norop --nosys >jump-gadgets.txt
