<!--
 * @encode: utf-8
 * @Date: 2025-04-05 15:18:16
 * @LastEditTime: 2025-04-12 13:31:58
 * @FilePath: /TD_mini_ICcard_tool/README.md
-->
# 这是一个简单的用于辅助查找IC卡某个数据块中的校验码的工具
目前仅支持单个字节的校验码

一次计算一个校验码
# 帮助信息:

```
#: python .\auto_get.py -h
usage: auto_get.py [-h] [-l LIMIT] -i INDEX [-s] -f FILE

命令行工具的说明

options:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        限制输出,如 '-l 3'即仅输出算法出现次数大于等于3的相关输出
  -i INDEX, --index INDEX
                        指定校验码在bytes类型时的下标
  -s, --skip            指定该参数,则跳过计算范围只有一个字符的情况
  -f FILE, --file FILE  指定输入的文件路径
```

# 使用示例:
1. 将多个发生变化了的数据块放入一个文件中,确保这些数据块的计算校验码的算法相同,每个数据块占一行(格式示例如block.txt)
2. `python -f block.txt -i 0 -l 10 -s`
    使用`-f`指定文件,`-i`指定校验码位置
    如:`0001B377001200000000D73D3DD70114`
    `-i 0` 即指定这个数据块的第一个`00`为要计算的校验码

    部分输出:
    ```
    #: python -f block.txt -i 0 -l 10 -s
    index:0 ('crc8', 6, 8): 10
    index:0 ('crc8', 6, 9): 10
    index:0 ('crc8', 7, 9): 10
    index:0 ('crc8', 6, 10): 10
    index:0 ('mod11_check', 6, 8): 10
    index:0 ('mod11_check', 6, 9): 10
    index:0 ('fletcher16', 6, 10): 10
    index:0 ('mod11_check', 7, 9): 10
    index:0 ('negation crc32', 8, 10): 10
    ```
    其中
    `index:0` 表示校验码的下标为0

    `'crc8'`与`'mod11_check'`这些为算法函数的名称,具体实现可以在`check_code_algorithm_func.py`中找到

    `('crc8', 6, 10): 10`中的`6`表示从数据块下标为6的位置的字节开始计算(包括下标为6的字节),第一个`10`表示到数据块下标为10的位置的字节结束计算(不包括下标为10的字节)
    如其中一个数据块如下:
    `0001B377001200000000D73D3DD70114`
    
    则`('crc8', 6, 10)`表示使用`crc8`函数计算`00000000`的校验码

    `('crc8', 6, 10): 10`最后一个`10`表示使用`('crc8', 6, 10)`计算了10个数据块,都正确

    `negation`表示`('crc8', 6, 10)`计算后取反,即使用`0xff`减去`('crc8', 6, 10)`的计算结果

    完整的说明
    
    `index:0 ('crc8', 6, 8): 10`
    
    将每一个数据块的下标为`0`的字节作为实际校验码
    使用`crc8`函数计算下标`6`到`8`(包括`6`不包括`8`)的字符串的校验码
    计算出的数值与实际校验码的数值相等的次数为`10`


# 扩展校验码算法

只需要在`check_code_algorithm_func.py`中添加算法函数,并且确保
1. 第一个参数为`data_bytes: bytes`
2. 并且有一个参数为`mask = 0xFF`
3. 返回值必须经过`return result & mask`计算确保返回值为两个字节的大小

具体示例参见`check_code_algorithm_func.py`的函数
