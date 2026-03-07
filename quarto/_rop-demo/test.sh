#!/bin/bash
mkfifo vulnout || true
mkfifo vulnin || true
strace -fo ptrace.out python3 attack.py >vulnin <vulnout &
strace -fo trace.out ./vulnerable <vulnin | tee vulnout
