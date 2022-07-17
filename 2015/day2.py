class Present:
    def __init__(self, *dims) -> None:
        self.width, self.length, self.height = dims

    @classmethod
    def parse_dimensions(cls, dims:str):
        return Present(*[int(dim) for dim in dims.split('x')])

    def __repr__(self) -> str:
        return f'width: {self.width}, length: {self.length}, height: {self.height}'

    def calculate_areas(self):
        wh = self.width*self.height
        wl = self.width*self.length
        hl = self.length*self.height

        surface_area = 2*sum([wh, wl, hl])

        smallest_area = min(wh, wl, hl)

        return surface_area + smallest_area

    def calculate_ribbon_length(self):
        return self.calculate_perimeter_ribbon() + self.calculate_bow_ribbon()

    def calculate_perimeter_ribbon(self):
        shortest, middle, longest = sorted([self.width, self.height, self.length])
        return 2*(shortest+middle)
    
    def calculate_bow_ribbon(self):
        return self.width*self.height*self.length


if __name__ == '__main__':
    with open('2015/day2.txt') as f:
        lines = f.read().rsplit()

    total_area = 0
    total_ribbon_length = 0

    for line in lines:
        present = Present.parse_dimensions(line)
        area = present.calculate_areas()
        total_area += area

        ribbon_length = present.calculate_ribbon_length()
        total_ribbon_length += ribbon_length

    print('Part1: ', total_area)
    print('Part2: ', total_ribbon_length)