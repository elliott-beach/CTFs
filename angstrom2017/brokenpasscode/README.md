The first step to this problem is to unzip the apk and decompile it with jadx.

The real code is in com/example/guest1/passcode_actf/MainActity.java:

![src](https://raw.githubusercontent.com/e-beach/CTFs/master/angstrom2017/brokenpasscode/MainActivity.png)

We can see that the key is read from a MetaData object property `"com.example.guest1.passcode_actf.key"`

Running `grep -rin 'com.example.guest1.passcode_actf.key'` from the root directory,
I discover the content is `AndroidManifest.xml`:

![xml](https://raw.githubusercontent.com/e-beach/CTFs/master/angstrom2017/brokenpasscode/AndroidManifest.png)
It looks the answer is `9999999`, but this flag doesn't work,
and the hint for the problem suggests we need to brute force the key somehow.

This had me stumped, but when I tried to run the apk in the Android Studio's Emulator, it gave me a signing error that
the hash for AndroidManifest.xml doesn't match.
Based on the problem description, it's now obvious that the value of `'com.example.guest1.passcode_actf.key'`
was modified after the apk was built, and we have to recover the original value.

It turns out that Android keeps an unsigned hash of every file in `META-INF/MANIFEST.MF`.
The catch is the *binary* version of AndroidManifest is the one that's signed, so we require
a little python trickery using `struct.pack` to find the location to edit in the binary file.

Checking the sha1 of the file with every possible int spits out the answer in about 20 seconds.
