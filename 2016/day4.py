
from collections import Counter
from string import ascii_lowercase
from typing import List
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Room:
    def __init__(self, encrypted_names: List[str], id: int, checksum: str) -> None:
        self.encrypted_names = encrypted_names
        self.id = id
        self.checksum = checksum
        
    @classmethod
    def parse_room_info(cls, info: str):
        room, checksum = info.strip().split('[')
        checksum = checksum.replace(']', '')
        *encrypted_names, id = room.split('-')
        return cls(encrypted_names, int(id), checksum)
    
    @property
    def isvalid(self):
        whole_name = ''.join(self.encrypted_names)
        char_count = Counter(whole_name)
        most_common_chars = char_count.most_common()
        sorted_chars = sorted(most_common_chars, key=(lambda char: (-char[1], char[0])))
        
        calculated_checksum = ''.join([char[0] for char in sorted_chars[:5]])
        return calculated_checksum == self.checksum
        
    def decrypt(self) -> str:
        '''
        Rotate each letters by ID
        '''
        decrypteds = []
        for name in self.encrypted_names:
            decrypted = ''
            for char in name:
                ind = ascii_lowercase.index(char)
                new_ind = (ind + self.id) % 26
                decrypted += ascii_lowercase[new_ind]
            decrypteds.append(decrypted)
        return ' '.join(decrypteds)
        
    def __repr__(self) -> str:
        return f'name {self.encrypted_names} id {self.id} checksum {self.checksum}'

@session.submit_result(level=1, tests=[({'inp': [
    'aaaaa-bbb-z-y-x-123[abxyz]',
    'a-b-c-d-e-f-g-h-987[abcde]',
    'not-a-real-room-404[oarel]',
    'totally-real-room-200[decoy]'
]}, 1514)])
def solve_part1(inp):
    rooms = [Room.parse_room_info(info) for info in inp if info]
    return sum(room.id for room in rooms if room.isvalid)

def test_decrypt():
    room = Room(encrypted_names=['qzmt', 'zixmtkozy', 'ivhz'], id=343, checksum='haha')
    room_decrypt = room.decrypt()
    assert room_decrypt == 'very encrypted name', f'test decrypt is {room_decrypt}'

@session.submit_result(level=2)
def solve_part2(inp):
    rooms = [Room.parse_room_info(info) for info in inp if info]
    decrypted_id_names = [(room.id, room.decrypt()) for room in rooms]
    northpole_room_id = [(id, room_name) for id, room_name in decrypted_id_names
                       if room_name == 'northpole object storage']
    np_id, np_name = northpole_room_id[0]
    return np_id


if __name__ == '__main__':
    inp = session.read_input().split('\n')
    solve_part1(inp)
    
    solve_part2(inp)
