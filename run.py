import numpy as np
from googletrans import Translator
from IPython import embed
from tqdm import tqdm
import os
#import re

def config_parser():
    """
    从命令行读取用户参数
    做出如下约定：
    1. -n 表示用户希望从自己所选择范围内具体想要复习的单词数量
    2. --r 表示用户希望随机选择单词（不输入 --r 则表示不希望随机选择）
    3. -s 表示用户希望从第几个单词开始
    4. -l 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
    5. -b 表示用户希望一次翻译多少单词集
    具体的边界条件请查看代码细节
    Returns:
        _type_: _description_
    """
    
    import configargparse
    parser = configargparse.ArgumentParser()
    parser.add_argument('--config', is_config_file=True, 
                        help='config file path')
    parser.add_argument("--basedir", type=str, default='./logs/', 
                        help='where to store word sets')
    parser.add_argument("--datadir", type=str, default='./', 
                        help='input data directory')
    parser.add_argument("--outname", type=str, default='my_review_words', 
                        help='output file name')
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        default=50,
        help="how many words would you like to review",
    )
    parser.add_argument(
        "--r",
        action="store_true",
        help="if you want to random select, then input --r, ohterwise do not",
    )
    parser.add_argument(
        '-s',
        '--start',
        type=int,
        default=0,
        help='which index to start reading from',
    )
    parser.add_argument(
        '-l',
        '--length',
        type=int,
        default=50,
        help='how many words would you randomly choose from',
    )
    parser.add_argument(
        '-b',
        '--batch',
        type=int,
        default=1,
        help='how many word sets would you make',
    )
    
    
    return parser

def run():
    parser = config_parser()
    args = parser.parse_args()
    for i in range(args.batch):
        make_set(i, args)

def make_set(index, args):
    in_filename = os.path.join(args.datadir,'collection.txt')
    out_filename0 = os.path.join(args.basedir,args.outname + f'_untrans_{index}.txt')
    out_filename1 = os.path.join(args.basedir,args.outname + f'_translated_{index}.txt')
    words = np.asarray(list(filter(None, open(in_filename,'r').read().split("\n"))))
    try:
        length , start, num = args.length , args.start, args.num
        if start + length > len(words):
            length = len(words) - start
        if num > length:
            num = length
        words = words[start:start + length]
        if args.r:
            words = np.random.choice(words, size=[num],replace=False)
        else:
            words = words[:num]
        print("collecting word",words.size)

        #写入未翻译words
        with open(out_filename0, "w") as f:
            for idx, each in enumerate(words):
                    similar_words = each.split(",")
                    f.write(f"{idx}:\t ")
                    for word in similar_words:
                        f.write(f"{word} ")
                    f.write("\n")
        
        # 设置Google翻译服务地址
        translator = Translator(service_urls=[
            'translate.google.cn'
        ])
        # 写入words & translated words
        with open(out_filename1, "w") as f:
            for i in tqdm(range(num)):
                similar_words = words[i].split(",")
                print('', similar_words)
                f.write(f"{i}:\t ")
                for word in similar_words:
                    try:
                        f.write(
                            word + ":" + translator.translate(word, dest='zh-CN').text + " " 
                        )
                    except Exception as e:
                        f.write(word + ":" + "翻译失败 ")
                f.write("\n")
        print("Done!")
    except Exception as e:
        embed(header=str(e))

if __name__ == "__main__":
    run()




