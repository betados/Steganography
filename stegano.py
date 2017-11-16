from PIL import Image


class Stegano(object):

    def encode(self, image, info='Aguangromanuer una peich ola k ase'):
        im = Image.open(image)
        px = im.load()
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


st = Stegano()

st.encode('clean.png')
print(st.decode('dirty.png'))
