# 简易拼音输入法

## 依赖

### 预处理
 - `jieba` 结巴分词
 - `pypinyin` 拼音注音
 - `tqdm` 显示进度条，可选

### 实际运行
 - 无

## 解释
 - `pin_yin_2.py`是字二元语法模型，`pin_yin_4.py`是字四元语法模型，它们依赖于`pre_processor_1.0.py`生成的数据；
 - `pin_yin_pro.py`是最终选定测试的算法版本（字二元+词二元），它依赖于`pre_processor_1.0.py`和`pre_processor_2.0.py`共同生成的数据。

## 用法
1. 获取语料，放入`raw`目录下；
2. 运行预处理程序（可能需要较长时间）；
3. 运行输入法程序。

## 声明
代码在上交作业之后还做过一些小改动，因此当前版本的代码效果可能与实验报告中描述的稍有不同。

## 附录
### 清华大学学生纪律处分管理规定实施细则
#### 第六章　学术不端、违反学习纪律的行为与处分
第二十一条 有下列违反课程学习纪律情形之一的，给予警告以上、留校察看以下处分：

（一）课程作业抄袭严重的；

（二）实验报告抄袭严重或者篡改实验数据的；

（三）期中、期末课程论文抄袭严重的；

（四）在课程学习过程中严重弄虚作假的其他情形。

（虽然我这个菜菜的代码应该也没人看。）