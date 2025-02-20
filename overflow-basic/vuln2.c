void vulnerable() {
  unsigned char needed_hash[32] = {...};
  unsigned char actual_hash[32];
  char buffer[100];
  gets(buffer);
  ComputeSHA256(buffer, actual_hash);
  if (memcmp(needed_hash,actual_hash,32)==0) {
    Interesting();
  }
}
