f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

class PacketInteger :
    def __init__(self, bits) :
        self._version = int(bits[0:3], 2)
        self._typeID = int(bits[3:6], 2) #should be 4 but let's keep it
        self._value, self._bitLen = self._decodeBits(bits)

    def __str__(self) :
        return f"<ver: {self._version}, bits: {self._bitLen}, val: {self._value}>"

    def staggerStr(self, depth) :
        return str(self)

    def _decodeBits(self, bits) :
        valBits = bits[6:]
        i = 0
        binVal = ""
        while True :
            binVal += valBits[1:5]
            i += 1
            if valBits[0] == "0" :
                break
            valBits = valBits[5:]

        value = int(binVal, 2)
        bitLen = 6 + i*5
        return value, bitLen

    def getBitLen(self) :
        return self._bitLen

    def versionNumSum(self) :
        return self._version

class PacketOperator :
    def __init__(self, bits) :
        self._version = int(bits[0:3], 2)
        self._typeID = int(bits[3:6], 2)
        self._lenType = int(bits[6])

        if self._lenType == 0 :
            self._len = int(bits[7:(7+15)], 2)
            subPacketsBits = bits[(7+15):]
            self._bitLen = 6 + 1 + 15
        else :
            self._len = int(bits[7:(7+11)], 2)
            subPacketsBits = bits[(7+11):]
            self._bitLen = 6 + 1 + 11

        self._subPackets = []

        self._decodeSubPackets(subPacketsBits)

    def __str__(self) :
        fullStr = self.staggerStr(1)
        fullStr += f"\nSum of version numbers: {self.versionNumSum()}"
        return fullStr

    def staggerStr(self, depth) :
        fullStr = f"ver: {self._version}, bits: {self._bitLen}, subPackets:"
        for pack in self._subPackets :
            fullStr = fullStr + "\n" + "   |"*depth + pack.staggerStr(depth + 1)
        return fullStr

    def versionNumSum(self) :
        vSum = self._version
        for pack in self._subPackets :
            vSum += pack.versionNumSum()
        return vSum

    def _decodeSubPackets(self, bits) :
        while True :
            if self._isFull() :
                break

            newType = int(bits[3:6], 2)

            if newType == 4 :
                newPacket = PacketInteger(bits)
            else :
                newPacket = PacketOperator(bits)

            newBitLen = newPacket.getBitLen()

            self._bitLen += newBitLen
            self._subPackets.append(newPacket)

            bits = bits[newBitLen:]

    def _isFull(self) :
        if self._lenType == 0 :
            return self._bitLen == self._len + 6 + 1 + 15
        else :
            return len(self._subPackets) == self._len

    def getBitLen(self) :
        return self._bitLen

hexaCode = L[0]
bits = bin(int(hexaCode, 16))[2:].zfill(len(hexaCode)*4)

print(hexaCode)
print(bits)

packet = PacketOperator(bits)
print(packet)
