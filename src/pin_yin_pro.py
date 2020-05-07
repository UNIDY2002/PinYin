from sys import argv
from time import strftime, localtime
from typing import Optional


class Candidate:
    def __init__(self, s: list, p: float, father: Optional['Candidate'], is_word: bool):
        self.s = s
        self.p = p
        self.father = father
        self.is_word = is_word

    def __str__(self) -> str:
        return ''.join(map(lambda x: x[0], self.s))

    def debug(self):
        print('[%s] %s %s %s' % ('W' if self.is_word else 'C', self.father, self, self.p))


def debug(s: str = ''):
    print(strftime('%H:%M:%S', localtime()), s)


def get_dict(src: str) -> dict:
    debug('Loading dictionary from %s ...' % src)
    data = open('../data/%s.txt' % src, encoding='utf-8')
    result = {}
    for line in data:
        line = line.strip()
        if ':' in line:
            key, val = line.split(':')
            result[key] = val.split(' ')
    return result


def get_cnt(src: str) -> tuple:
    debug('Loading key-count from %s ...' % src)
    data = open('../data/%s.txt' % src, encoding='utf-8')
    cnt = int(data.readline().strip())
    result = {}
    for line in data:
        line = line.strip()
        if ' ' in line:
            key, val = line.split(' ')
            result[key] = int(val)
    return cnt, result


def get(src: dict, *args: list) -> int:
    s = '/'.join(map(lambda x: ','.join(map(lambda y: '%s:%s' % (y[0], y[1]), x)), args))
    return src[s] if s in src else 0


if __name__ == '__main__':
    char_dict = get_dict('chars')
    word_dict = get_dict('words')
    char_cnt, char_mem = get_cnt('char_cnt')
    word_cnt, word_mem = get_cnt('word_cnt')
    _, phrase_mem = get_cnt('phrase_cnt')
    debug('Start processing.')

    input_file = open(argv[1] if len(argv) > 1 else '../data/input.txt', encoding='utf-8')
    output_file = open(argv[2], 'w', encoding='utf-8') if len(argv) > 2 else None
    for input_line in input_file:
        if input_line.strip() == '':
            continue
        debug(input_line.strip())
        pin_yin_list = input_line.strip().lower().split(' ')
        history = [[Candidate([], 1, None, False)]]

        for i in range(len(pin_yin_list)):
            candidates = []
            chars = char_dict[pin_yin_list[i]]
            for c in chars:
                notated = [(c, pin_yin_list[i])]
                max_c = max(map(lambda x: (x, x.p * (
                        get(phrase_mem, x.s, notated) / (get(word_mem, x.s) + 1)
                        * (12 if x.is_word else
                           (5 if len(x.s) == 1 and '%s:%s' % (x.s[0][0], x.s[0][1]) in word_mem else 0)) +
                        ((get(char_mem, x.s + notated) / (get(char_mem, x.s) + 1) * 8) if len(x.s) > 0 else 0) +
                        (get(char_mem, notated) + 1) / char_cnt)), history[-1]), key=lambda x: x[1])
                candidates.append(Candidate(notated, max_c[1], max_c[0], False))

            for length in range(2, min(6, i) + 2):
                pin_yin = pin_yin_list[i + 1 - length: i + 1]
                pin_yin_str = ' '.join(pin_yin)
                words = word_dict[pin_yin_str] if pin_yin_str in word_dict else []
                for w in words:
                    notated = list(map(lambda x, y: (x, y), w, pin_yin))
                    max_c = max(map(lambda x: (x, x.p * (
                            get(phrase_mem, x.s, notated) / (get(word_mem, x.s) + 1)
                            * (666 if x.is_word else
                               (404 if (len(x.s) == 1 and '%s:%s' % (x.s[0][0], x.s[0][1]) in word_mem) else 0)) +
                            ((get(char_mem, x.s + notated) / (get(char_mem, x.s) + 1) * 233) if len(x.s) > 0 else 0)
                            + get(word_mem, notated) / word_cnt * 50 * (len(notated)) ** 2)),
                                    history[-length]), key=lambda x: x[1])
                    candidates.append(Candidate(notated, max_c[1], max_c[0], True))
            history.append(candidates)

        current = max(history[-1], key=lambda x: x.p)
        ans = ''
        while current:
            ans = str(current) + ans
            current = current.father
        debug(ans)
        if output_file:
            output_file.write(ans + '\n')
