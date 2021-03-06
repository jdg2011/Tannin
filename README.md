# Tannin
### Disintegrated hash storage for Tea.lock
A small command-line program that stores hashes (i.e. encrypted passwords) generated by Tea.lock in a disintegrated state so as to totally eliminate malicious access to usable hashes, all while maintaining ease of use.

Keywords, used to identify hashes, are stored in a plaintext file, water.txt, while the hashes are halved and stored in two separate files, earl.txt and grey.txt.

Tea.lock encrypts text with at a two-for-one character rate. For example, input `a` results in output `bc`. If `a = bc`, it follows that `bc = a`; also, `b = ?` and `c = ?`. In other words, `a` is unknowable without both `b` and `c` present.

That means plaintext encrypted with Tea.lock is unknowable without the full hash. Tannin's hash dividing function allows you to store the two hash files necessary for decryption in separate locations, so that if one of the two locations is compromised, no data is at risk.
