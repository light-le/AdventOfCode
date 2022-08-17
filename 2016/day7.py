
from functools import reduce
from re import findall, match, search
from typing import List, Set, Tuple
import doctest
from more_itertools import sliding_window, triplewise
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

def extract_brackets(inp: str) -> Tuple[List[str], List[str]]:
    insides = findall('\[(\w+)\]', inp)
    outsides = findall('\](\w+)\[', inp)
    outside_before = match('^(\w+)\[', inp)
    if outside_before:
        outsides = [outside_before.group(1)] + outsides
    outside_after = search('\](\w+)$', inp)
    if outside_after:
        outsides.append(outside_after.group(1)) 
    return outsides, insides

def test_extract_brackets():
    inp_expecteds = [
        ('a[b]c', (['a', 'c'], ['b'])),
        ('abc[def]ghi', (['abc', 'ghi'], ['def'])),
        ('ab[cd][ef]gh', (['ab', 'gh'], ['cd', 'ef'])),
        ('ab[cd]gh[ef]', (['ab', 'gh'], ['cd', 'ef'])),
        ('[cd][ef]', ([], ['cd', 'ef'])),
    ]
    for inp, expected in inp_expecteds:
        output = extract_brackets(inp)
        assert expected == output, f'Input {inp}. Calculated {output}. Expected {expected}'

def is_abba(w: Tuple[str, ...]) -> bool:
    '''
    >>> is_abba(('a','b','b','a'))
    True
    >>> is_abba(('a','a','a','a'))
    False
    >>> is_abba(('a','b','c','a'))
    False
    >>> is_abba(('a','b','b','c'))
    False
    '''
    first, sec, third, fourth = w
    if first != sec and first == fourth and sec == third:
        return True
    return False

def look_for_abba(txt: str) -> bool:
    windows_of_4 = sliding_window(txt, 4)
    for window in windows_of_4:
        if is_abba(window):
            return True
    return False        
    

@session.submit_result(level=1, tests=[({'inp': (gen for gen in [
    'abba[mnop]qrst',
    'abcd[bddb]xyyx',
    'aaaa[qwer]tyui',
    'ioxxoj[asdfgh]zxcvbn',
    ])}, 2)])
def solve_part1(inp: List):
    bracket_extractions = (extract_brackets(i) for i in inp)
    ip_count = 0
    for outsides, insides in bracket_extractions:
        if any(look_for_abba(o) for o in outsides) and not any(look_for_abba(i) for i in insides):
            ip_count+=1
    return ip_count

def is_aba(tri: Tuple[str, ...]) -> bool:
    '''
    >>> is_aba(('a', 'b', 'a'))
    True
    >>> is_aba(('a','a','a'))
    False
    >>> is_aba(('a','b','b'))
    False
    '''
    first, sec, third = tri
    if first == third and first != sec:
        return True
    return False

def is_bab(tri: Tuple[str, ...]) -> bool:
    return is_aba(tri)

def extract_abas(txt: str) -> Set[str]:
    triplechars = triplewise(txt)
    abas = set()
    for tripchar in triplechars:
        if is_aba(tripchar):
            abas.add(''.join(tripchar))
    return abas

def extract_babs(txt: str) -> Set[str]:
    return extract_abas(txt)

def convert_aba_to_bab(aba: str) -> str:
    '''
    >>> convert_aba_to_bab('aba')
    'bab'
    >>> convert_aba_to_bab('aaa')
    'aaa'
    >>> convert_aba_to_bab('bba')
    'bbb'
    '''
    first = aba[0]
    sec = aba[1]
    return sec + first + sec

@session.submit_result(level=2, tests=[({'inp': [
    'aba[bab]xyz',
    'xyx[xyx]xyx',
    'aaa[kek]eke',
    'zazbz[bzb]cdb'
]}, 3)])
def solve_part2(inp):
    bracket_extractions = (extract_brackets(i) for i in inp)
    ssl_count = 0
    for outsides, insides in bracket_extractions:
        extracted_abas = (extract_abas(o) for o in outsides)
        abas = reduce((lambda set_a, set_b: set_a | set_b), extracted_abas)
        
        converted_babs = {convert_aba_to_bab(aba) for aba in abas}
        extracted_babs = reduce((lambda set_a, set_b: set_a | set_b),
                                (extract_babs(i) for i in insides))
        if converted_babs & extracted_babs:
            ssl_count+=1
    return ssl_count

if __name__ == '__main__':
    test_extract_brackets()
    doctest.testmod()
    inp = [i for i in session.read_input().split('\n') if i]
    
    solve_part1(inp)
    
    solve_part2(inp)
