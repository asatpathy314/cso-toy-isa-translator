import re

class Translator:
    def __init__(self, file_path):
        with open(file_path, "r") as f:
            commands = f.read()
        arr_bin = self.convert(commands)
        pC = 0
        self.readable = ''
        for x in range(len(arr_bin)):
            if x!=pC:
                continue
            concat, incPC = self.translation_bin_to_isa(arr_bin[x], pC)
            concat = "Instruction: " + f"{(int(arr_bin[x], 2)):02x}".upper() + " " + concat + '\n'
            pC+=  incPC
            self.readable += concat

    def get_bits(self, number, idx1, idx2):
        """Returns the bits of number between idx1 and idx2 as an integer"""
        if idx1 > idx2:
            low, num = idx2, idx1-idx2
        else:
            low, num = idx1, idx2-idx1
        return (number >> low) & ((1 << num)-1)
    
    def convert(self, bits):
        """ 
        Takes a string of hex commands in and
        and outputs an arr of commands in binary.
        """
        bits.replace("0x", "")
        arr_hex_str = re.sub(r'[^a-zA-Z0-9]+', ' ', bits).strip().split(" ")
        arr_bin = [format(int(x, 16),  '#010b') for x in arr_hex_str]
        return arr_bin

    def translation_bin_to_isa(self, instruction, oldPC):
        """
        Converts binary command into a human-understandable string
        """

        instruction = int(instruction, 2)
        reserved = self.get_bits(instruction, 7, 8)
        icode = self.get_bits(instruction, 4, 7)
        a = self.get_bits(instruction, 2, 4)
        b = self.get_bits(instruction, 0, 2)

        decoded =  '; '.join(["pC: " + f"{(oldPC):02d}", "Reserved: " + str(reserved), "iCode: " + str(icode), "rA: "+ str(a), "rB: " + str(b), "Instruction: "])
        
        if(reserved == 1 and icode == 7):
            decoded += "Stop"
            return decoded, 0
        match icode:
            case 0:
                if(reserved==0):
                    decoded += "R[a] = R[b]"
                elif(reserved==1):
                    match b:
                        case 0:
                            decoded += "RSP -= 1; M[RSP] = R[a]"
                            return decoded.replace('a', str(a)), 1
                        case 1:
                            decoded += "R[a] = M[RSP]; RSP += 1"
                            return decoded.replace('a', str(a)), 1
                        case 2:
                            decoded += "RSP += 1; M[RSP] = oldPC+2; pC = M[pC+1]"
                            return decoded.replace('a', str(a)), 2
                        case 3:
                            decoded += "RSP -= 1; pc = M[RSP+1]"
                            return decoded.replace('a', str(a)), 2
            case 1:
                decoded += "R[a] = R[a] + R[b]"
            case 2: 
                decoded += "R[a] = R[a] & R[b]"
            case 3:
                decoded += "R[a] = M[R[b]]"
            case 4:
                decoded += "M[R[b]] = R[a]"
            case 5:
                match b:
                    case 0:
                        decoded += "R[a] = ~R[a]"
                    case 1:
                        decoded += "R[a] = -R[a]"
                    case 2:
                        decoded += "R[a] = !R[a]"
                    case 3:
                        decoded += "R[a] = oldPC"
                return decoded.replace('a', str(a)), 1
            case 6:
                match b:
                    case 0:
                        decoded += "R[a] = M[oldPC+1]"
                    case 1:
                       decoded += "R[a] = R[a] + M[oldPC+1]"
                    case 2:
                        decoded += "R[a] = R[a] & M[oldPC+1]"
                    case 3:
                        decoded += "R[a] = M[M[oldPC+1]]"
                return decoded.replace('a', str(a)).replace('oldPC+1', str(oldPC+1)), 2
            case 7:
                decoded += "if(R[a] <= 0): pC = R[b]"
        return decoded.replace('a', str(a)).replace('b', str(b)), 1
    
if __name__ == "__main__":
    trans = Translator("./programs/test")
    print(trans.readable)