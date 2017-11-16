from PIL import Image


class Stegano(object):

    def encode(self, image, info=12345):
        im = Image.open(image)
        px = im.load()
        try:
            info = str(info)
        except:
            exit()
        for i, char in enumerate(info):
            binario = bin(int(char))[2:]
            while len(binario) < 4:
                binario = '0' + binario
            for j, bit in enumerate(binario):
                auxList = [v for v in px[i, j][:3]]
                alpha = bin(px[i, j][3])
                alpha = alpha[:-1] + bit
                alpha = int(alpha, 2)
                auxList.append(alpha)
                px[i, j] = tuple(v for v in auxList)
                # print(px[i, j])
                # print('\n')
            im.save('dirty.png')



    def decode(self, image):
        im = Image.open(image)
        px = im.load()
        numero = ''
        for i in range(9):
            binario = ''
            for j in range(4):
                binario += bin(px[i, j][3])[-1]
            numero += str(int(binario,2))
        return int(numero)

st = Stegano()

st.encode('clean.png')
print(st.decode('dirty.png'))
