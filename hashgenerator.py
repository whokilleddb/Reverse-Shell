import hashlib

val = input("[+] Enter String To Hash : ")
hashval = hashlib.sha1(val.encode('utf-8')).hexdigest()
hashval = str(hashval)
print(f"[+] Hash Value = {hashval}")
