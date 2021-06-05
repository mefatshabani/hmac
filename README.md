# hmac
 Hash functions - A hash function is a function that takes an arbitrary block of data and returns afixed-size unique bit string representation


-----------------------------
# Some questions realted to HMAC (Hash Functions)
-----------------------------

<h3> What are the properties of a cryptographic hash function? </h3>

1. Easy to compute hash value (fast) <br>
2. Hard to restore message from hash (one-way) <br>
3. Hard to find messages with the same hash (collision resistant) <br>
4. Similar messages have very different hashes (avalanche effect) <br>
<br> 

<h3> What attacks must a cryptographic hash function resist? </h3>

Collision, First and Second Preimage attacks. When a collision attack is discovered and is found to be faster than a birthday attack, a hash function is often denounced as "broken"
<br><br>

<h3> What does the size of the output from a hash function influence? </h3>

The security level of the CryptoSystem
<br><br>

<h3> What is a “security level” in cryptography? </h3>

If a cryptosystem which has a 56-bit key can be brute-forced using 2**56 operations, then the cryptosystem has a security level of 56 bits
<br><br>

<h3> What is the commitment scheme useful for? </h3>

A commitment scheme is a cryptographic primitive that allows one to commit to a chosen value (or chosen statement) while keeping it hidden to others, with the ability to reveal the committed value later.
<br>
<br>
<h3> Why is it better to store hashed passwords in a db? </h3>

Because if someone breaks into the db, still can not know them (supposing they all have a high level of ramdomness)
<br><br>

<h3> How can we increase the security level of password hashing? </h3>

Adding a salt
<br><br>

<h3> How can we create an encryption scheme from a hash function? </h3>

Using a Feistel Network, to make a block cipher.
"By hashing K||n where K is the secret key and n is a counter. Then, XORing this key-dependent pseudo-random stream with the data to encrypt, you have a stream cipher."
<br><br>

<h3> What is HMAC useful for? </h3>

For checking message integrity, Digital Signature
<br><br>

<h3> Why is using MD5/SHA1 for HMAC not insecure? </h3>

Because MD5 and SHA1 have known attacks that makes retrieving the hash primitive computationally feasible
<br><br>


-----------------------------
# Testing
-----------------------------

In the same folder where test files, test script and hmac files are located:

$ chmod +x hmac.py <br>
$ chmod +x test_hmac.sh <br>

$ sed -i 's/\r//g' hmac.py <br>
$ sed -i 's/\r//g' test_hmac.sh <br>

finally, we execute the script and follow the instructions, writing the correct keys:

$ ./test_hmac.sh
