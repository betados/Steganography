#!/usr/bin/env python3

""" Stegano hides a string within an image.
It puts each bit of the ascii code of each char in the LSB of each channel of a RGBA image """

from PIL import Image
import argparse


class Stegano(object):
    # ascii code max bit length
    """only 7 is needed, made it 8 to be multiple of the four channels.
    This way each char is hided in two pixels"""
    length = 8

    # TODO add encryption option

    @staticmethod
    def encode(info, image, imageOut='dirty.png'):
        try:
            im = Image.open(image)
        except:
            print("No such image", image)
            exit()
        px = im.load()
        if isinstance(px[0, 0], int) or len(px[0, 0]) != 4:
            im = im.convert("RGBA")
            px = im.load()
        try:
            info = str(info)
        except:
            exit()

        line = 0
        x = 0
        lineWidth, lineCant = im.size
        for char in info:
            binario = Stegano.char2binario(char)
            try:
                auxList1 = [int(bin(v)[:-1] + bit, 2) for v, bit in zip(px[x, line], binario[:4])]
                auxList2 = [int(bin(v)[:-1] + bit, 2) for v, bit in zip(px[x+1, line], binario[4:])]
                px[x, line] = tuple(v for v in auxList1)
                px[x+1, line] = tuple(v for v in auxList2)
                x += 2
                if x >= lineWidth-1:
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
        binario = bin(ord(char))[2:]
        while len(binario) < Stegano.length:
            binario = '0' + binario
        return binario

    @staticmethod
    def decode(image):
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
                auxList2 = [bin(v)[-1] for v in px[x+1, line]]
                auxList = auxList1 + auxList2
                code = ''.join(auxList)
                x += 2
                if x >= lineWidth-1:
                    line += 1
                    x = 0
            except Exception as e:
                print(e)
                break

            info += chr(int(code, 2))
        return info[:-1]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--encode",
                        help="Encode the given string into given image. "
                             "\nIf the string contains spaces type it \"between quotes\"",
                        nargs=2,
                        metavar=('STRING', 'IMAGE'))
    parser.add_argument('-o', "--output", help="Output image when encoding", nargs=1, metavar='IMAGE')
    parser.add_argument("-d", "--decode", help="Decode from the given image", nargs=1, metavar='IMAGE')

    args = parser.parse_args()

    if args.encode:
        if args.output:
            Stegano.encode(args.encode[0], args.encode[1], args.output[0])
        else:
            Stegano.encode(args.encode[0], args.encode[1])
        print('Encoded')
    if args.decode:
        if args.output:
            print("Output image is an argument only valid for encoding.")
        print(Stegano.decode(args.decode[0]))
