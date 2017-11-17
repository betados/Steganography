from PIL import Image
import argparse


class Stegano(object):
    def encode(self, info, image):
        im = Image.open(image)
        px = im.load()
        if isinstance(px[0, 0], int):
            print("image is B&W, only RGBA supported for now")
            exit()
        if len(px[0, 0]) != 4:
            print("Only RGBA supported for now")
            exit()
        try:
            info = str(info)
        except:
            exit()

        for i, char in enumerate(info):
            binario = bin(ord(char))[2:]
            while len(binario) < 7:
                binario = '0' + binario
            for j, bit in enumerate(binario):
                auxList = [v for v in px[i, j][:3]]
                alpha = bin(px[i, j][3])
                alpha = alpha[:-1] + bit
                alpha = int(alpha, 2)
                auxList.append(alpha)
                px[i, j] = tuple(v for v in auxList)
        im.save('dirty.png')

    def decode(self, image):
        im = Image.open(image)
        px = im.load()
        info = ''
        code = ''
        i = 0
        while i == 0 or 31 < int(code, 2) < 127:
            code = ''
            for j in range(7):
                code += bin(px[i, j][3])[-1]
            info += chr(int(code, 2))
            i += 1
        return info[:-1]


if __name__ == "__main__":
    st = Stegano()

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--encode",
                        help="Encode given string into given image. "
                             "\nIf the string contains spaces type it \"between quotes\"",
                        nargs=2,
                        metavar=('STRING', 'IMAGE'))
    parser.add_argument("-d", "--decode", help="Decode from given image", nargs=1, metavar='IMAGE')
    args = parser.parse_args()
    # print(args.decode)
    # print(args.encode)

    if args.encode:
        st.encode(args.encode[0], args.encode[1])
        print('Encoded')
    if args.decode:
        print(st.decode(args.decode[0]))
