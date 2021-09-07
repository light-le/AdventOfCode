from itertools import permutations
from time import sleep
import day5

part1_test = {
    43210: "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",
    54321: "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
    65210: "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
}

def solve_part1(inp):
    perms = permutations(range(5))
    max_thrust = 0
    for perm in perms:
        amp_input = 0
        for phase in perm:
            amplifier = day5.Codes2(map(int, inp.split(',')), amp_input)
            amplifier.codes[amplifier.codes[1]] = phase
            i = 2
            while i < amplifier.len:
                code = amplifier.codes[i]
                if code == 1:
                    amplifier.program1(i)
                    i+=4
                elif code == 2:
                    amplifier.program2(i)
                    i+=4
                elif code == 3:
                    amplifier.program3(i)
                    i+=2
                elif code == 4:
                    amp_input = amplifier.codes[amplifier.codes[i+1]]
                    i+=2
                elif code == 5:
                    i = amplifier.program5(i)
                elif code == 6:
                    i = amplifier.program6(i)
                elif code == 7:
                    amplifier.program7(i)
                    i+=4
                elif code == 8:
                    amplifier.program8(i)
                    i+=4
                elif code > 99:
                    if str(code)[-1] == 4:
                        amp_input = amplifier.codes[i+1]
                        i+=2
                    else:
                        i=amplifier.pro_param(i)
                elif code == 99:
                    break
        max_thrust = max(amp_input, max_thrust)
    return max_thrust


for output, input in part1_test.items():
    cal_output = solve_part1(input)
    assert output == cal_output, f"Test fails. Expected output {output}, got {cal_output} instead."

with open('day7.txt', 'r') as f:
    part1_input = f.readline().rstrip()
    print(f"All tests for part1 passed, the actual output for part1 is {solve_part1(part1_input)}")

part2_test = {
    139629729: ('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5', [9,8,7,6,5]),
    18216: ('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10', [9,7,8,5,6]),
}

def solve_part2(inp, exp_output, exp_seq):
    """
    Few problems I see here with how you're reading it - I'm not sure what you mean by "change the phase setting to zero.", and also you mention "When coming back to A, use the first phase setting and after that the output from E (last amplifier)." which implies you're restarting the intcode machine every time.

You should be running 5 intcode machines, and they run once from start to finish. During that time they may prompt for input that you may or may not be currently able to provide. If you can't, you need to wait until you can and then provide it and continue from there (no restarting.)

Longer:

Create 5 instances of your intcode computer (with their own separate Program Counters and memory), A - E. During the execution, they will at various points try to OUTPUT or INPUT (opcodes 3 + 4).

They then run as follows:

A takes 2 inputs (phase, "0"), outputs a value, then tries to take a 3rd that you don't have yet, so pause it (store the memory and PC AS-IS) and move on to B.

B takes 2 inputs (phase, Output from A), outputs a value, then tries to take a 3rd that you don't have yet, so pause it and move on to C

C, repeats the same, but using "Output from B" for the second input.

D, repeats the same, but using "Output from C" for the second input.

E, repeats the same, but using "Output from D" for the second input.

Now you can loop back to A. You now have the value from E that you can use to provide that 3rd input, it'll run for a while (continuing from where you paused it earlier, not from the beginning) and eventually it will output another value and wait for a 4th input. Pause it, move on to B.

B's 3rd input is output A gave after being given it's 3rd input from E's output, it will do the same again, consume the input, generate an output, then wait for a 4th input.

And so on, each amplifier will consume the previous output and generate a new one then wait for more input.

Eventually, they'll all stop asking for input and actually halt (Opcode 99) all basically at the same time in order (A, then B, then C...) once E has halted take the output and that's your answer.

(When they halt, they'll provide an output before halting, so you'll still have something to pass on to the next amplifier when it asks for an input)
    """
    max_thrust = 0
    for perm in [exp_seq]: #permutations(range(5,10)):
        amp_input = 0
        count = 0
        while max_thrust < exp_output:
            count+=1
            for phase in perm:
                amplifier = day5.Codes2(map(int, inp.split(',')), amp_input)
                amplifier.codes[amplifier.codes[1]] = phase
                i = 2
                while i < amplifier.len:
                    code = amplifier.codes[i]
                    if code == 1:
                        amplifier.program1(i)
                        i+=4
                    elif code == 2:
                        amplifier.program2(i)
                        i+=4
                    elif code == 3:
                        amplifier.program3(i)
                        i+=2
                    elif code == 4:
                        amp_input = amplifier.codes[amplifier.codes[i+1]]
                        i+=2
                    elif code == 5:
                        i = amplifier.program5(i)
                    elif code == 6:
                        i = amplifier.program6(i)
                    elif code == 7:
                        amplifier.program7(i)
                        i+=4
                    elif code == 8:
                        amplifier.program8(i)
                        i+=4
                    elif code > 99:
                        if str(code)[-1] == 4:
                            amp_input = amplifier.codes[i+1]
                            i+=2
                        else:
                            i=amplifier.pro_param(i)
                    elif code == 99:
                        break
            max_thrust = max(amp_input, max_thrust)
            print('max thrust: ', max_thrust, ' count: ', count)
    return max_thrust


for output, (input, exp_seq) in part2_test.items():
    cal_output = solve_part2(input, output, exp_seq)
    assert output == cal_output, f"Test fails. Expected output {output}, got {cal_output} instead"
