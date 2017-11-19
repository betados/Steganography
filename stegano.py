#!/usr/bin/env python3

""" Stegano hides a string within an image.
It puts each bit of the ascii code of each char in the LSB of the alpha channel of a RGBA image """

from PIL import Image
import argparse


class Stegano(object):
    # ascii code max bit length
    length = 7

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
        lineWidth = im.size[0]
        for i, char in enumerate(info):
            if i == lineWidth:
                line += 1
            binario = bin(ord(char))[2:]
            while len(binario) < Stegano.length:
                binario = '0' + binario
            try:
                for j, bit in enumerate(binario):
                    # todo use every channel
                    auxList = [v for v in px[i - line * lineWidth, j + line * Stegano.length][:3]]
                    alpha = bin(px[i - line * lineWidth, j + line * Stegano.length][3])
                    alpha = alpha[:-1] + bit
                    alpha = int(alpha, 2)
                    auxList.append(alpha)
                    px[i - line * lineWidth, j + line * Stegano.length] = tuple(v for v in auxList)
            except:
                print('No cupo todo!')
                break
        im.save(imageOut)

    @staticmethod
    def decode(image):
        try:
            im = Image.open(image)
        except:
            print("No such image", image)
            exit()
        px = im.load()
        info = ''
        code = ''
        i = 0
        line = 0
        lineWidth = im.size[0]
        while i == 0 or 31 < int(code, 2) < 127:
            code = ''
            if i == lineWidth:
                line += 1
            try:
                for j in range(Stegano.length):
                    code += bin(px[i - line * lineWidth, j + line * Stegano.length][3])[-1]
            except:
                break
            info += chr(int(code, 2))
            i += 1
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
