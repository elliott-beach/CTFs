# Broken Passcode

Description: My friend was holding his passcode checker tool, but he was too busy looking at his screen and he tripped! Now the passcode has fallen out of the code and out of his brain. See if you can recover [it](https://github.com/e-beach/CTFs/blob/master/angstrom2017/brokenpasscode/brokenpasscode.apk?raw=true).

Hint: There are no repeats in the digits of the correct passcode. If you find something that has repeats, maybe that's becuase my friend dropped it... also he suddenly had an epiphany and remembered that he hates 0s, and his passcode doesn't have any...

### Solution

The first step to this problem is to unzip the apk (that is, an Android app) and decompile it with jadx.

The real code is in`com/example/guest1/passcode_actf/MainActity.java`:

![src](https://raw.githubusercontent.com/e-beach/CTFs/master/angstrom2017/brokenpasscode/MainActivity.png)

We can see that the key is read from a MetaData object property `"com.example.guest1.passcode_actf.key"`.
Running `grep -rin 'com.example.guest1.passcode_actf.key'` from the root directory,
I discover the content is in the decompilied version of `AndroidManifest.xml`:

![xml](https://raw.githubusercontent.com/e-beach/CTFs/master/angstrom2017/brokenpasscode/AndroidManifest.png)


It looks the answer is `9999999`, but this flag doesn't work,
and the hint for the problem suggests we need to brute force the key somehow.

This had me stumped, so I tried to run the apk in Android Studio's emulator.
This gave me a signing error that the signature for AndroidManifest.xml is incorrect.
Based on this error and the problem description, it's now obvious that the value of `'com.example.guest1.passcode_actf.key'`
was modified after the apk was built, and we have to recover the original value.

After poking around a little, I discover that signed apps have a SHA-1 hash of every file in `META-INF/MANIFEST.MF`.
Knowing the hash, we can guess values for the key until we find a version of AndroidManifest which matches the original hash.
We know the key is an integer, probably less than `999999`, with no 0s or repeats.
The catch is the *binary* version of AndroidManifest is the one that's signed, so we require
a little python trickery using `struct.pack` to find the location to edit in the binary file.


Checking with every possible int spits out `8195472` in about 20 seconds ([code](https://github.com/e-beach/CTFs/blob/master/angstrom2017/brokenpasscode/passcode_soln.py)).


