from sys import argv
from time import strftime, localtime


class Candidate:
    def __init__(self, s: str, p: float, father: str):
        self.s = s
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
        history = [[Candidate('   ', 1, '   ')]]

        for i in range(len(pin_yin_list)):
            pin_yin_0 = pin_yin_list[i]
            pin_yin_1 = pin_yin_list[i - 1] if i > 0 else ''
            pin_yin_2 = pin_yin_list[i - 2] if i > 1 else ''
            pin_yin_3 = pin_yin_list[i - 3] if i > 2 else ''
            chars = char_map[pin_yin_0]
            candidates = []
            for c in chars:
                max_dict = {}
                threshold = 0
                for x in history[-1]:
                    prev = x.s[1:3]
                    prev_3 = (x.s[0], pin_yin_3)
                    prev_2 = (x.s[1], pin_yin_2)
                    prev_1 = (x.s[2], pin_yin_1)
                    prev_0 = (c, pin_yin_0)
                    prob = x.p * (cnt(prev_3, prev_2, prev_1, prev_0) /
                                  (cnt(prev_3, prev_2, prev_1) + 1) * 5 +
                                  cnt(prev_2, prev_1, prev_0) /
                                  (cnt(prev_2, prev_1) + 1) * 8 +
                                  cnt(prev_1, prev_0) /
                                  (cnt(prev_1) + 1) * 6 +
                                  cnt(prev_0) / all_char_len)
                    if prob > 0 and (prev not in max_dict or prob > max_dict[prev][1]):
                        max_dict[prev] = (x, prob)
                    if prob > threshold:
                        threshold = prob

                threshold /= 120
                for key in max_dict:
                    if max_dict[key][1] >= threshold:
                        candidates.append(Candidate(max_dict[key][0].s[1:3] + c, max_dict[key][1], max_dict[key][0].s))
            history.append(candidates)

        candidate = max(history[-1], key=lambda can: can.p)
        ans = candidate.s[2]
        for p_candidates in history[-2:0:-1]:
            for p_c in p_candidates:
                if p_c.s == candidate.father:
                    candidate = p_c
                    ans = p_c.s[2] + ans
                    break
        print(time(), ans)
        if output_data:
            output_data.write(ans + '\n')
