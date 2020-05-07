from time import strftime, localtime

import jieba
from pypinyin import lazy_pinyin
from tqdm import tqdm

if __name__ == '__main__':
    word_count = 0
    word_mem = {}
    phrase_mem = {}
    word_dict = {}


    def add_word(word: str, pin_yin: list) -> int:
        if ' ' not in word:
            add_key = ','.join(map(lambda x, y: '%s:%s' % (x, y), word, pin_yin))
            word_mem[add_key] = word_mem[add_key] + 1 if add_key in word_mem else 1
            pin_yin = ' '.join(pin_yin)
            if pin_yin in word_dict:
                word_dict[pin_yin].add(word)
            else:
                word_dict[pin_yin] = {word}
            return 1
        else:
            return 0


    def add_phrase(word_1: str, pin_yin_1: list, word_2: str, pin_yin_2: list):
        if ' ' not in word_1 and ' ' not in word_2:
            add_key_1 = ','.join(map(lambda x, y: '%s:%s' % (x, y), word_1, pin_yin_1))
            add_key_2 = ','.join(map(lambda x, y: '%s:%s' % (x, y), word_2, pin_yin_2))
            add_key = '%s/%s' % (add_key_1, add_key_2)
            phrase_mem[add_key] = phrase_mem[add_key] + 1 if add_key in phrase_mem else 1


    for index in range(10):
        print("%s Processing %d..." % (strftime("%H:%M:%S", localtime()), index))
        corpora_data = open('../raw/%d.txt' % index, encoding='utf-8')

        for line in tqdm(corpora_data):
            data = line.strip()
            seg_list = list(jieba.tokenize(data))
            pin_yin_list = lazy_pinyin(data)
            for i in range(len(seg_list)):
                word_count += add_word(seg_list[i][0], pin_yin_list[seg_list[i][1]: seg_list[i][2]])
                if i < len(seg_list) - 1:
                    add_phrase(seg_list[i][0], pin_yin_list[seg_list[i][1]: seg_list[i][2]],
                               seg_list[i + 1][0], pin_yin_list[seg_list[i + 1][1]: seg_list[i + 1][2]])

    word_corpora = open('../data/word_cnt.txt', 'w', encoding='utf-8')
    word_corpora.write("%d\n" % word_count)
    for key in word_mem:
        word_corpora.write("%s %d\n" % (key, word_mem[key]))

    phrase_corpora = open('../data/phrase_cnt.txt', 'w', encoding='utf-8')
    phrase_corpora.write('0\n')
    for key in phrase_mem:
        if phrase_mem[key] > 8:
            phrase_corpora.write('%s %d\n' % (key, phrase_mem[key]))

    words = open('../data/words.txt', 'w', encoding='utf-8')
    for key in word_dict:
        words.write("%s:%s\n" % (key, ' '.join(word_dict[key])))
