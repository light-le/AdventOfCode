from abc import ABC
from typing import List
from utils import AdventSession, extract_year_day_from_path



session = AdventSession(**extract_year_day_from_path(__file__))

class Component(ABC):
    def __init__(self, name: str, parent_folder: object=None) -> None:
        self.name = name
        self.parent_folder = parent_folder
        
        if parent_folder is not None:
            parent_folder.children.append(self)
        
    @property
    def full_path(self):
        parent_folder_names = list()
        current = self
        while current.parent_folder:
            parent_folder_names.append(current.parent_folder.name)
            current = current.parent_folder

        return '/'.join(parent_folder_names[::-1] + [self.name])
    
    @property
    def size(self):
        return 0

    def __repr__(self) -> str:
        return f'{self.name} {self.size}'
        
class File(Component):
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size: int):
        self._size = size
        
class Folder(Component):
    def __init__(self, name: str, parent_folder: object=None) -> None:
        super().__init__(name, parent_folder)
        self.children = list()
        
    @property
    def size(self) -> int:
        return sum(child.size for child in self.children)
    

@session.submit_result(level=1, tests=[({'inp': [
    '$ cd /',
    '$ ls',
    'dir a',
    '14848514 b.txt',
    '8504156 c.dat',
    'dir d',
    '$ cd a',
    '$ ls',
    'dir e',
    '29116 f',
    '2557 g',
    '62596 h.lst',
    '$ cd e',
    '$ ls',
    '584 i',
    '$ cd ..',
    '$ cd ..',
    '$ cd d',
    '$ ls',
    '4060174 j',
    '8033020 d.log',
    '5626152 d.ext',
    '7214296 k'
]}, 95437)])
def solve_part1(inp: List[str]):
    all_folders = parse_command(inp)
                
    return sum(folder.size for folder in all_folders.values() if folder.size <= 1e5)

def parse_command(inp):
    line = 0
    all_folders = {
        '/': Folder('/')
    }

    while line < len(inp):
        if inp[line] == '$ cd ..':
            current_folder = current_folder.parent_folder
            line+=1
        elif inp[line].startswith('$ cd'):
            dollar, cd, folder_name = inp[line].split()
            if folder_name == '/':
                current_folder = all_folders['/']
            else:
                current_folder = all_folders[f'{current_folder.full_path}/{folder_name}']
            line+=1
        elif inp[line] == '$ ls':
            line += 1
            while line < len(inp) and not inp[line].startswith('$'):
                if inp[line].startswith('dir'):
                    dir, dir_name = inp[line].split()
                    folder = Folder(dir_name, current_folder)
                    all_folders[folder.full_path] = folder
                else:
                    file_size, file_name = inp[line].split()
                    file = File(file_name, current_folder)
                    file.size = int(file_size)
                line += 1
    return all_folders

@session.submit_result(level=2, tests=[({'inp': [
    '$ cd /',
    '$ ls',
    'dir a',
    '14848514 b.txt',
    '8504156 c.dat',
    'dir d',
    '$ cd a',
    '$ ls',
    'dir e',
    '29116 f',
    '2557 g',
    '62596 h.lst',
    '$ cd e',
    '$ ls',
    '584 i',
    '$ cd ..',
    '$ cd ..',
    '$ cd d',
    '$ ls',
    '4060174 j',
    '8033020 d.log',
    '5626152 d.ext',
    '7214296 k'
]}, 24933642)])
def solve_part2(inp):
    all_folders = parse_command(inp)
    total_disk_space = 70000000
    unused_space = total_disk_space-all_folders['/'].size
    space_needed = 30000000 - unused_space
    
    folder_that_can_be_deleted = [folder for folder in all_folders.values() if folder.size >= space_needed]
    return min(folder.size for folder in folder_that_can_be_deleted)
    


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
