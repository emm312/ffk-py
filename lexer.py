from enum import Enum

class TokenType(Enum):
    ADD = 1
    SUB = 2
    START_INFINITE_LOOP = 3
    END_LOOP = 4
    HEX_NUMBER = 5


    HEX_PORT_IN = 6
    HEX_PORT_OUT = 7

    PORT_IN = 8
    PORT_OUT = 9

    OUT_REG_ASCII = 10
    IN_REG_ASCII = 11


    PUSH = 12
    POP = 13
    LOOP_COUNTER = 14
    HEX_LOOP = 15

class Token:
    def __init__(self, content: str, type: TokenType) -> None:
        self.type = type
        self.content = content
    def fmt(self) -> str:
        return self.type.name + ": " + self.content


def tokenise(src: str) -> list[Token]:
    toks: list[Token] = []
    i = 0
    while i < len(src):
        currchar = src[i]
        if currchar == "$":
            toks.append(Token("$", TokenType.LOOP_COUNTER))
            i += 1
            continue
        elif currchar == "0":
            number = src[i+1] + src[i+2]
            srcidx = src[i+3]
            if srcidx == "[":
                token_type = TokenType.HEX_LOOP
            elif srcidx == "<":
                token_type = TokenType.HEX_PORT_IN
            elif srcidx == ">":
                token_type = TokenType.HEX_PORT_OUT
            
            toks.append(Token(number, token_type))
            i += 4
            continue
        elif currchar == "?":
            if src[i+1] == "<":
                toks.append(Token("?<", TokenType.POP))
            elif src[i+1] == ">":
                toks.append(Token("?>", TokenType.PUSH))
            else:
                print("?????????????????????????? what da ? doin????")
                exit(-1)
            i += 2
            continue
        elif currchar == "]":
            toks.append(Token("]", TokenType.END_LOOP))
            i += 1
            continue
        elif currchar == "[":
            toks.append(Token("[", TokenType.START_INFINITE_LOOP))
        elif currchar == "+":
            toks.append(Token("+", TokenType.ADD))
            i += 1
            continue
        elif currchar == "-":
            toks.append(Token("-", TokenType.SUB))
            i += 1
            continue
        elif currchar == "<":
            toks.append(Token("<", TokenType.IN_REG_ASCII))
            i += 1
            continue
        elif currchar == ">":
            toks.append(Token(">", TokenType.OUT_REG_ASCII))
            i += 1
            continue
        elif currchar == "%":
            j = 1
            port_name = "%"
            while True:
                if src[i+j] == "%":
                    break
                else:
                    port_name += src[i+j]
                j += 1
            j += 1
            if src[i+j] == ">":
                toks.append(Token(port_name, TokenType.PORT_OUT))
            elif src[i+j] == "<":
                toks.append(Token(port_name, TokenType.PORT_IN))
            i += j+1
            continue
        i+=1
    return toks
        