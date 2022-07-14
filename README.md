# sast2022_words_translator

a navie script for words-translation

## Installation
- Clone this repo by `git clone https://github.com/Axian12138/sast2022_words_translator`
- Python>=3.6 (installation via anaconda is recommended, use `conda create -n words_review python=3.9` to create a conda environment and activate it by `conda activate words_review`)
- Python libraries
    - Install core requirements by `pip install -r requirements.txt`

## running
If you have completed the installation. Then, for example:

`python run.py --config config.txt`  config.txt中保存希望的参数，可参照当前路径下的config.txt

or

`python run.py -n 50` 主要参数含义如下

- -n 表示用户希望从自己所选择范围内具体想要复习的单词数量
- --r 表示用户希望随机选择单词（不输入 --r 则表示不希望随机选择）
- -s 表示用户希望从第几个单词开始
- -l 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
- -b 表示用户希望一次翻译多少单词集

