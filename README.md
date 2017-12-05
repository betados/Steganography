# Steganography
An script to hide and retrieve information within photographs.
It puts each bit of the ascii code of each char in the LSB of each channel of a RGBA image.
It has the option to hide it encrypted via AES algorithm.

usage: steganos.py [-h] [-e IMAGE] [-o IMAGE] [-d IMAGE] [-p PASSWORD]

optional arguments:
* -h, --help  -->  show this help message and exit
* -e IMAGE, --encode IMAGE  -->  Encode given string into given image.
* -o IMAGE, --output IMAGE --> Output image when encoding
* -d IMAGE, --decode IMAGE  -->  Decode from given image
* -p, --password --> In case you want to hide the message encripted or you want to retrive an encripted one.
A hidden prompt will appear when intro is pressed



Dependencies:
* Pycryptodome: pip install pycryptodome

or
* pip install -r requirements.txt
