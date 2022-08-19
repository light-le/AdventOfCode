
import doctest
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Marker:
    def __init__(self, m: str) -> None:
        self.chars, self.repeat = [int(s) for s in m.split('x')]
        

def decompress(string: str) -> str:
    '''
    >>> decompress('ADVENT')
    'ADVENT'
    >>> decompress('A(1x5)BC')
    'ABBBBBC'
    >>> decompress('(3x3)XYZ')
    'XYZXYZXYZ'
    >>> decompress('A(2x2)BCD(2x2)EFG')
    'ABCBCDEFEFG'
    >>> decompress('(6x1)(1x3)A')
    '(1x3)A'
    >>> decompress('X(8x2)(3x3)ABCY')
    'X(3x3)ABC(3x3)ABCY'
    '''
    string = string.replace(' ', '')
    decompressed = []
    c = 0
    while c < len(string):
        char = string[c]
        if char == '(':
            for d in range(c+4, len(string)):
                if string[d] == ')':
                    marker = Marker(string[c+1:d])
                    c = d + marker.chars
                    
                    repeated_string = string[d+1:c+1]*marker.repeat
                    decompressed.extend(list(repeated_string))
                    break
        else:
            decompressed.append(char)
        c+=1        
    return ''.join(decompressed)

@session.submit_result(level=1, tests=[({'inp': [
    'ADVENT',
    'A(1x5)BC',
    '(3x3)XYZ',
    'A(2x2)BCD(2x2)EFG',
    '(6x1)(1x3)A',
    'X(8x2)(3x3)ABCY',
]}, 57)])
def solve_part1(inp):
    return sum((len(decompress(i)) for i in inp))

def recursive_decompress(string: str) -> str:
    '''
    >>> recursive_decompress('X(8x2)(3x3)ABCY')
    'XABCABCABCABCABCABCY'
    >>> recursive_decompress('(3x3)XYZ')
    'XYZXYZXYZ'
    '''
    decompressed = string
    while '(' in decompressed:
        decompressed = decompress(decompressed)
    return decompressed

class Decompressed(str):
    def decompress_length(self) -> int:
        if not '(' in self:
            return len(self)
        open_i = self.index('(')
        initial_len = open_i
        close_i = self.index(')')
        
        marker = Marker(self[open_i+1: close_i])
        decom_len = Decompressed(self[close_i+1:close_i+1+marker.chars]).decompress_length()*marker.repeat
        next_decom_len = Decompressed(self[close_i+1+marker.chars:]).decompress_length()
        return initial_len+decom_len+next_decom_len
            

@session.submit_result(level=2, tests=[({'inp': [
    '(3x3)XYZ',
    'X(8x2)(3x3)ABCY',
    '(27x12)(20x12)(13x14)(7x10)(1x12)A',
    '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN',
]}, 9+20+241920+445)])
def solve_part2(inp):
    return sum(Decompressed(i).decompress_length() for i in inp)


if __name__ == '__main__':
    doctest.testmod()
    inp = [i for i in session.read_input().split('\n') if i]
    
    solve_part1(inp)
    
    solve_part2(inp)
