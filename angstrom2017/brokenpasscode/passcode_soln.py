import struct
import hashlib
from base64 import b64encode, b64decode

expected = b64decode('F0T3vG9oImHgTmMPeAu0dfJ0sVk=')
key = struct.pack('i', 9999999)
contents = open('AndroidManifest.xml', 'rb').read()
assert key in contents

for i in range(9999999):
    if len(set(str(i).replace("0", ""))) == len(str(i)):
        if hashlib.sha1(contents.replace(key, struct.pack('i', i))).digest() == expected:
            print("matched for i=%d" % i)
            break

# matched for i=8195472
