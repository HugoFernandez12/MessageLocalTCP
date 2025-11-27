from operator import xor


class bufferTCP:

    def __init__(self, _size):
        self.buffering = b""
        self.size = _size

    # ----------------------------------------------------------------------
    def encapsulateMsg(self, text):
        crc = bytes([self.calculateCrc(b'\x02' + text.encode() + b'\x03')])
        text = b'\x02' + text.encode() + b'\x03' + crc + b'\x04'
        print(f"TEXTO A MANDAR {text} ----- CRC {crc}")
        return text
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    def addMsg(self, text):
        if (len(self.buffering) + len(text)) <= self.size:
            self.buffering = self.buffering + text
        else:
            self.buffering = b""
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    def extractMsg(self):
        message = b""
        characterCrc = b""
        deleteControl = 0
        for x in range(0, len(self.buffering)):
            if self.buffering[x] == 0x02:
                msgControl = x
                for y in range(msgControl + 1, len(self.buffering)):
                    if self.buffering[y] == 0x02:
                        msgControl = y
                    elif self.buffering[y] == 0x04:
                        deleteControl = y
                        for z in range(msgControl + 1, y):
                            if self.buffering[z] == 0x03:
                                for w in range(z + 1, y):
                                    characterCrc = characterCrc + bytes([self.buffering[w]])

                                break
                            else:
                                message = message + bytes([self.buffering[z]])
                        break
                break
        if deleteControl != 0:
            self.buffering = self.buffering[deleteControl + 1:len(self.buffering)]
        if self.validateCrc(characterCrc, message):
            return message.decode()
        else:
            return "ERROR"
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    @staticmethod
    def calculateCrc(text):
        y = 0
        for x in text:
            y = xor(x, y)
        return (y + 32) % 256
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    def validateCrc(self, characterCrc, text):
        text = b'\x02' + text + b'\x03'
        if characterCrc != b"":
            y = self.calculateCrc(text)
            print(f"CHARACTER CRC {characterCrc} --- BYTES {bytes([y])}")
            if characterCrc == bytes([y]):
                return True
            else:
                return False
        else:
            return True
    # ----------------------------------------------------------------------
