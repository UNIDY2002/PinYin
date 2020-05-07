if __name__ == '__main__':
    output = list(filter(lambda x: x.strip() != '', open('../data/output.txt', encoding='utf-8').readlines()))
    standard = list(filter(lambda x: x.strip() != '', open('../data/standard.txt', encoding='utf-8').readlines()))
    correct_line = correct_char = total_char = 0
    if len(output) != len(standard):
        print('\033[31m总行数不匹配！\033[0m')
    else:
        total_line = len(standard)
        for i in range(total_line):
            out, std = output[i].strip(), standard[i].strip()
            total_char += len(std)
            if len(out) != len(std):
                print('\033[31;43m%s\033[0m' % out)
            else:
                correct = True
                for j in range(len(std)):
                    if out[j] != std[j]:
                        print('\033[31m%s\033[0m' % out[j], end='')
                        correct = False
                    else:
                        print(out[j], end='')
                        correct_char += 1
                print()
                if correct:
                    correct_line += 1
        print('字：%d/%d = %f' % (correct_char, total_char, correct_char / total_char))
        print('句：%d/%d = %f' % (correct_line, total_line, correct_line / total_line))
