#!/usr/bin/env python3

""" Steganos hides a string within an image.
It puts each bit of the ascii code of each char in the LSB of each channel of a RGBA image.
It has the option to hide it encrypted via AES algorithm
"""

from PIL import Image
import argparse
import encryption as crypto
from getpass import getpass


class Steganos(object):
    # ascii code max bit length
    """only 7 is needed, made it 8 to be multiple of the four channels.
    This way each char is hided in two pixels"""
    length = 8

    @staticmethod
    def encode(info, image, imageOut, password):
        try:
            im = Image.open(image)
        except:
            print("No such image", image)
            exit()
        if not imageOut:
            imageOut = 'dirty.png'
        else:
            imageOut = imageOut[0]
        px = im.load()
        if isinstance(px[0, 0], int) or len(px[0, 0]) != 4:
            im = im.convert("RGBA")
            px = im.load()
        try:
            info = str(info)
        except:
            exit()

        if password:
            info = crypto.encrypt(info, password)

        line = 0
        x = 0
        lineWidth, lineCant = im.size
        for char in info:
            binario = Steganos.char2binario(char)
            try:
                auxList1 = [int(bin(v)[:-1] + bit, 2) for v, bit in zip(px[x, line], binario[:4])]
                auxList2 = [int(bin(v)[:-1] + bit, 2) for v, bit in zip(px[x + 1, line], binario[4:])]
                px[x, line] = tuple(v for v in auxList1)
                px[x + 1, line] = tuple(v for v in auxList2)
                x += 2
                if x >= lineWidth - 1:
                    line += 1
                    x = 0
                if line > lineCant:
                    print('No cupo todo!')
                    break
            except:
                print('No cupo todo!')
                break
        im.save(imageOut)

    @staticmethod
    def char2binario(char):
        # print(char)
        binario = bin(ord(char))[2:]
        while len(binario) < Steganos.length:
            binario = '0' + binario
        return binario

    @staticmethod
    def decode(image, password):
        try:
            im = Image.open(image)
        except:
            print("No such image", image)
            exit()
        px = im.load()
        info = ''
        x = 0
        line = 0
        lineWidth = im.size[0]
        while x == 0 or 31 < int(code, 2) < 127:
            try:
                auxList1 = [bin(v)[-1] for v in px[x, line]]
                auxList2 = [bin(v)[-1] for v in px[x + 1, line]]
                auxList = auxList1 + auxList2
                code = ''.join(auxList)
                x += 2
                if x >= lineWidth - 1:
                    line += 1
                    x = 0
            except Exception as e:
                print(e)
                break

            info += chr(int(code, 2))

        if password:
            return crypto.decrypt(info[:-1], password)
        return info[:-1]


if __name__ == "__main__":
    # FIXME problema gordo de seguridad. EL historial de la terminal recuerda todo lo tecleado

    parser = argparse.ArgumentParser(description="""An script to hide and retrieve information within photographs.
It puts each bit of the ascii code of each char in the LSB of each channel of a RGBA image.
It has the option to hide it encrypted via AES algorithm.""")
    parser.add_argument("-e", "--encode",
                        help="Encode the given string into given image. "
                             "\nIf the string contains spaces type it \"between quotes\"",
                        nargs=2,
                        metavar=('STRING', 'IMAGE'))
    parser.add_argument('-o', "--output", help="Output image when encoding", nargs=1, metavar='IMAGE')
    parser.add_argument("-d", "--decode", help="Decode from the given image", nargs=1, metavar='IMAGE')
    parser.add_argument('-p', '--password', action='store_true', dest='password',
                        help="hidden password prompt in case you want to hide the message encriptedor "
                             "you want to retrive an encripted one. The longer the better, up to 20 chars")

    args = parser.parse_args()

    password = None
    if args.password:
        password = getpass()

    if args.encode and not args.decode:
        Steganos.encode(args.encode[0], args.encode[1], args.output, password)
        print('Encoded')
    if args.decode and not args.encode:
        if args.output:
            print("Output image is an argument only valid for encoding.")
        print(Steganos.decode(args.decode[0], password))

    if args.decode and args.encode:
        print("You cannot encode and decode in the same execution")
