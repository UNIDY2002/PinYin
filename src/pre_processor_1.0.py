from time import strftime, localtime

import jieba
from pypinyin import lazy_pinyin
from tqdm import tqdm

if __name__ == '__main__':
    all_char_len = 0
    mem = {}


    def put(items: list):
        s = ','.join(map(lambda p: "%s:%s" % (p[0], p[1]), items))
        w = 2 if items[len(items) - 1][2] == items[0][2] or items[0][3] else 1
        mem[s] = mem[s] + w if s in mem else w


    for index in range(10):
        print("%s Processing %d..." % (strftime("%H:%M:%S", localtime()), index))
        corpora_data = open('../raw/%d.txt' % index, encoding='utf-8')

        for line in tqdm(corpora_data):
            data = line.strip().replace(' ', '')
            all_char_len += len(data)
            seg_list = jieba.lcut(data, cut_all=False)
            pin_yin_list = lazy_pinyin(data)

            notated = []
            cur_char = 0
            for i in range(len(seg_list)):
                for j in range(len(seg_list[i])):
                    notated.append((seg_list[i][j], pin_yin_list[cur_char], i, j == 0))
                    cur_char += 1

            for i in range(len(notated)):
                put([notated[i]])
                if i < len(notated) - 1:
                    put(notated[i:i + 1])
                if i < len(notated) - 2:
                    put(notated[i:i + 2])
                if i < len(notated) - 3:
                    put(notated[i:i + 3])

    pre_processed_data = open('../data/char_cnt.txt', 'w', encoding='utf-8')
    pre_processed_data.write("%d\n" % all_char_len)
    for key in mem:
        if ',' not in key or mem[key] > 20:
            pre_processed_data.write("%s %d\n" % (key, mem[key]))
