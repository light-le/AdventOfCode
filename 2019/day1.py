with open('day1.txt', 'r') as f:
    lines = f.readlines()

mass = [int(line.rstrip()) for line in lines]

def calculate_fuel(m):
    return max(m//3 - 2, 0)

total_fuel = 0
for m in mass:
    fuel = calculate_fuel(m)
    while fuel > 0:
        total_fuel+=fuel
        fuel = calculate_fuel(fuel)
print(total_fuel)