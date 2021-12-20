def convert_9tiles_to_binary(x, y, imgd, step):
    pixel_to_binary = {'.': '0', '#': '1'}
    pixels = ''
    outer = '.' if step % 2 == 0 else '#'

    for yi in range(y-1, y+2):
        for xi in range(x-1, x+2):
            pixels += imgd.get((xi, yi), outer)
    binary = ''.join([pixel_to_binary[p] for p in pixels])
    return binary

def solution(imgd, algo, steps):
    for step in range(steps):
        new_imgd = imgd.copy()
        for x in range(-1-step, 102+step):
            for y in range(-1-step, 102+step):
                binary_9tiles = convert_9tiles_to_binary(x, y, imgd, step)
                output_pixel = algo[int(binary_9tiles, 2)]
                new_imgd[(x,y)] = output_pixel
        imgd = new_imgd
    return list(imgd.values()).count('#')

if __name__ == "__main__":
    with open('2021/day20.txt', 'r') as f:
        lines = f.readlines()

        algo, linebreak, *image = lines
        image = [img.rstrip() for img in image]
        image_dict = dict()

        for r, row in enumerate(image):
            for c, col in enumerate(row):
                image_dict[(c, r)] = col

        print(solution(image_dict, algo, steps=2))
        print(solution(image_dict, algo, steps=50))
