from random import randint
class coder:
    def __init__(self):
        self.key = ''
        self.generateKey()
    
    def encode(self, data):
        data = data[::-1]
        data = list(data)
        j= 0
        for i,item in enumerate(data):
            next_pos = ord(item) + ord(self.key[j])
            while next_pos > 126:
                next_pos = 32+(next_pos-126)
            data[i] = chr(next_pos)
            j+=1
            if j == len(self.key):
                j = 0
            if i % 2 != 0:
                temp = data[i-1]
                data[i-1]= data[i]
                data[i] = temp
        return ''.join(data)


    def decode(self, data):
        j = 0
        data = list(data)
        for i,item in enumerate(data):
            if i%2 == 0 and i<len(data)-1:
                temp = data[i+1]
                data[i+1]= data[i]
                data[i] = temp
        for i,item in enumerate(data):
            next_pos = ord(item) - ord(self.key[j])
            while next_pos <32:
                next_pos = -32+(next_pos+126)
            data[i] = chr(next_pos)
            j+=1
            if j == len(self.key):
                j = 0

        return ''.join(data)[::-1]

    def generateKey(self):
        for i in range(128):
            self.key+=chr(randint(32,126))


if __name__ == '__main__':
    coder = coder()

    code = coder.encode('Every inch of wall space is covered by a bookcase. Each bookcase has six shelves, going almost to the ceiling. Some bookshelves are stacked to the brim with hardback books: science, maths, history, and everything else. Other shelves have two layers of paperback science fiction, with the back layer of books propped up on old tissue boxes or lengths of wood, so that you can see the back layer of books above the books in front. And it still isn’t enough. Books are overflowing onto the tables and the sofas and making little heaps under the windows.')
    key = coder.key
    print(code)