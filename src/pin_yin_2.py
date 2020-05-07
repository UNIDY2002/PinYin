from sys import argv
from time import strftime, localtime


class Candidate:
    def __init__(self, char: str, p: float, father: str):
        self.char = char
        self.p = p
        self.father = father


def time() -> str:
    return strftime("%H:%M:%S", localtime())


if __name__ == '__main__':
    print(time(), "start")
    char_data = open('../data/chars.txt', encoding='utf-8')
    char_map = {}
    for line in char_data:
        chars = line.strip().split(':')
        char_map[chars[0]] = chars[1].split(' ')

    corpora_data = open('../data/char_cnt.txt', encoding='utf-8')
    all_char_len = int(corpora_data.readline())
    mem = {}
    for line in corpora_data:
        if ' ' in line:
            key, count = line.strip().split(' ')
            count = int(count)
            mem[key] = count


    def cnt(*args: tuple) -> int:
        valid = []
        for char in args:
            if char != '' and char != ' ':
                valid.append("%s:%s" % (char[0], char[1]))
        s = ','.join(valid)
        return mem[s] if s in mem else 0


    input_data = open(argv[1] if len(argv) > 1 else '../data/input.txt', encoding='utf-8')
    output_data = open(argv[2], 'w', encoding='utf-8') if len(argv) > 2 else None
    for line in input_data:
        print(time(), line.strip())
        pin_yin_list = line.strip().lower().split(' ')
        history = [[Candidate('', 1, '')]]

        for i in range(len(pin_yin_list)):
            pin_yin = pin_yin_list[i]
            prev = pin_yin_list[i - 1] if i > 0 else ''
            chars = char_map[pin_yin]
            candidates = []
            for c in chars:
                m = max(map(lambda x: (x, x.p * (cnt((x.char, prev), (c, pin_yin)) / (cnt((x.char, prev)) + 1) * 150 +
                                                 cnt((c, pin_yin)) / all_char_len)), history[-1]), key=lambda x: x[1])
                candidates.append(Candidate(c, m[1], m[0].char))
            history.append(candidates)

        candidate = max(history[-1], key=lambda x: x.p)
        ans = candidate.char
        for p_candidates in history[-2::-1]:
            for p_c in p_candidates:
                if p_c.char == candidate.father:
                    candidate = p_c
                    ans = p_c.char + ans
                    break
        print(time(), ans)
        if output_data:
            output_data.write(ans + '\n')
