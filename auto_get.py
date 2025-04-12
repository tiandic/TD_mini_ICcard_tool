import inspect
import argparse
import check_code_algorithm_func

def list_functions_in_module(module):
    """
    列出给定模块中的所有函数名称。

    参数:
    module: 要检查的模块对象。

    返回:
    list: 包含模块中所有函数名称的列表。
    """
    functions = [name for name, obj in inspect.getmembers(module, inspect.isfunction)]
    return functions


def call_function_from_module(function_name, *args, **kwargs):
    """
    从模块 check_code_algorithm_func 中调用指定名称的函数，并传递参数。

    参数:
    function_name (str): 要调用的函数名称。
    *args: 要传递给函数的位置参数。
    **kwargs: 要传递给函数的关键字参数。

    返回:
    调用函数的返回值。

    异常:
    AttributeError: 如果在模块中找不到指定名称的函数。
    TypeError: 如果找到的对象不可调用。
    """
    # 从模块中获取函数对象
    func = getattr(check_code_algorithm_func, function_name, None)
    if func is None:
        raise AttributeError(f"模块 'check_code_algorithm_func' 中未找到函数 '{function_name}'。")
    if not callable(func):
        raise TypeError(f"对象 '{function_name}' 不是可调用的函数。")
    # 调用函数并传递参数
    return func(*args, **kwargs)

def get_command_line_args():
    parser = argparse.ArgumentParser(description="命令行工具的说明")
    parser.add_argument("-l","--limit",type=int,default=0,help="限制输出,如 '-l 3'即仅输出算法出现次数大于等于3的相关输出")
    parser.add_argument("-i","--index",type=int,default=0,help="指定校验码在bytes类型时的下标")
    parser.add_argument("-s","--skip" ,action='store_true',help="指定该参数,则跳过计算范围只有一个字符的情况")
    parser.add_argument("-f","--file",type=str,required=True,help="指定输入的文件路径")
    parser.add_argument("--auto",action='store_true',help="尝试自动寻找校验码算法(自动模式下,不指定-l时,仅会输出完全符合所有数据块的算法)")
    args = parser.parse_args()
    return args

def get_one_checkcode_algorithm(args):
    
    file=open(args.file,encoding="utf-8")
    func_list=list_functions_in_module(check_code_algorithm_func)

    # 获取校验码下标
    checkcode_NO=args.index


    doc={}
    # 字典格式:
    #    {[函数,计算位置的开始下标,计算位置的结束下标] : 出现次数}
    for i in file.readlines():
        # 去除 \n
        block=i.strip()

        block_bytes=bytes.fromhex(block)
        # 实际校验码
        rignt_check_code=block_bytes[checkcode_NO]
        # 获取数据的所有组合
        for start_no_block_bytes in range(len(block_bytes)):
            for end_no_block_bytes in range(start_no_block_bytes+1,len(block_bytes)):
                # 使用check_code_algorithm_func.py的所有算法计算校验码
                for func in func_list:
                    check_code=call_function_from_module(func,block_bytes[start_no_block_bytes:end_no_block_bytes])
                    if check_code == rignt_check_code:
                        # 字典的键
                        doc_key=(func,start_no_block_bytes,end_no_block_bytes)
                        if doc_key in doc:
                            doc[doc_key]=doc[doc_key]+1
                        else:
                            doc[doc_key]=1
                    # 单字节取反
                    elif 0xff-check_code == rignt_check_code:
                        # 字典的键
                        doc_key=(f"negation {func}",start_no_block_bytes,end_no_block_bytes)
                        if doc_key in doc:
                            doc[doc_key]=doc[doc_key]+1
                        else:
                            doc[doc_key]=1
    file.close()
    sorted_data = dict(sorted(doc.items(), key=lambda item: (-item[1], len(str(item[0])))))

    # 获取限制输出的指定
    lim=args.limit

    # 指定则跳过计算范围只有一个字符的情况
    sk_one=args.skip

    for key,value in sorted_data.items():
        # 按照算法出现次数,限制输出
        if value >= lim:
            # 排除实际校验码出现在用于计算校验码的范围中
            if not (checkcode_NO >=key[1] and checkcode_NO <key[2]):
                if not (sk_one and key[2]-key[1]==1):
                    print(f"index:{args.index} {key}: {value}")
    return doc

def main():
    args=get_command_line_args()

    # 自动模式
    if args.auto:
            with open(args.file) as f:
                total_lines=f.readlines()
                total_line_num=len(total_lines)
            # print(total_lines[0])
            with open(args.file) as f:
                frist_line=f.readline().strip()
                # print(type(frist_line))
                line_len=int(len(frist_line)/2)
            if args.limit==0:
                # 自动模式下,不指定-l时,仅会输出完全符合所有数据块的算法
                args.limit=total_line_num
            # 将每一个字节都当成校验码
            for i in range(line_len):
                args.index=i
                get_one_checkcode_algorithm(args)
    else:
        # 非自动模式
        get_one_checkcode_algorithm(args)




if __name__ == '__main__':
    main()