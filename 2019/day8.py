from functools import reduce
from os import replace

with open('day8.txt', 'r') as f:
    line = f.readline()
    nums = [int(c) for c in line]


def solve_part1(nums):
    layer_area = 25*6
    layers = [nums[i:i+layer_area] for i in range(0, len(nums), layer_area)]
    layer_0_count = [layer.count(0) for layer in layers]
    fewest_0_layer = layers[layer_0_count.index(min(layer_0_count))]
    return fewest_0_layer.count(1) * fewest_0_layer.count(2)

print(solve_part1(nums))

class Layer:
    def __init__(self, inp, width=25, tall=6) -> None:
        self.pixels = [inp[i:i+width] for i in range(0, width*tall, width)]
    def __repr__(self) -> str:
        def convert_bw(p):
            return '.' if p == 1 else ' '
        return '\n'.join([''.join([convert_bw(p) for p in row]) for row in self.pixels])
    def flatten_layer(self) -> list:
        return reduce(lambda a, b: a+b, self.pixels)
    def merge_layers(self, next):
        # 2 would be replaced by whatever follows
        def replace2(t, n):
            return n if t == 2 else t
        merged = [replace2(this_pixel, next_pixel) for this_pixel, next_pixel in zip(self.flatten_layer(), next.flatten_layer())]
        return Layer(merged, len(self.pixels[0]), len(self.pixels))

def solve_part2(nums):
    layer_area = 25*6
    layers = [Layer(nums[i:i+layer_area]) for i in range(0, len(nums), layer_area)]
    final_layer = reduce(lambda a,b: a.merge_layers(b), layers)
    return final_layer

print(solve_part2(nums))