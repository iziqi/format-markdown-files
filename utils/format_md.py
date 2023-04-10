# useful functions

import re, os, shutil
from utils.dirs import clear_folder


def split_md(note):
    '''
    按照一二级标题分割文件，一级标题为文件夹，
    每个二级标题及其内容为该文件夹下的单独md文件
    Split the given markdown file:
    First create different folders by top-level headings
    then split markdown files by second-level headings
    '''
    # 设置保存分割后文件的文件夹
    note_name = os.path.splitext(note)[0].split('\\')[-1]
    separate_folder = os.path.join(os.path.dirname(note), note_name + ' seperated')
    clear_folder(separate_folder)

    with open(note, 'r', encoding='utf-8') as f:
        text = f.readlines()
    count = 0
    check_top_level = 0
    for line in text:
        if re.search(r'^#\s+', line):  # 匹配一级标题：'# XXXXX'
            check_top_level += 1
            tmp_folder_name = line[2:].replace('\n', '')  # 提取一级标题作为文件夹名
            tmp_folder_path = os.path.join(separate_folder, tmp_folder_name)
            # shutil.rmtree(tmp_folder_path, ignore_errors=True)  # 清空目标文件夹
            if not os.path.exists(tmp_folder_path):
                os.makedirs(tmp_folder_path)
        elif re.search(r'^##\s+', line):  # 匹配二级标题：'## XXXXX'
            if check_top_level == 0:
                print('Split md error: second-level heading appears before top-level heading.')
                return 
            if count != 0:  # 排除第一次经过，保存上一个二级标题下的内容
                with open(separate_note_path, 'a', encoding='utf-8') as f:
                    f.write(seperate_note_text)
            count += 1
            separate_note_name = line[3:].replace('\n', '')  # 提取二级标题为md文件名
            separate_note_path = os.path.join(
                tmp_folder_path, separate_note_name + '.md'
            )
            seperate_note_text = '# ' + separate_note_name + '\n'  # 二级标题名称作为md开头
        elif re.search(r'.', line, re.S):  # 匹配正文和换行，匹配所有内容
            if count != 0:
                seperate_note_text += line
    if count != 0:  # 处理文件结尾的最后一个二级标题
        with open(separate_note_path, 'a', encoding='utf-8') as f:
            f.write(seperate_note_text)
    print(f'Split md done.')

def merge_md_helper(notes_folder, contents):
    '''
    递归合并notes_folder中的所有md文件，内容保存为contents
    '''
    if os.path.isfile(notes_folder): # 到单独文件了，退出条件
        with open(notes_folder, 'r', encoding='utf-8') as f:
            contents.append(f.read() + '\n')
        return contents
    
    for note in os.listdir(notes_folder):
        note_path = os.path.join(notes_folder, note)
        if os.path.isdir(note_path):
            contents.append(f'# {note}' + '\n') # 将文件夹名保存为1级标题
            contents = merge_md_helper(note_path, contents)
        else:
            with open(note_path, 'r', encoding='utf-8') as f:
                contents.append(f.read() + '\n')
    return contents

def merge_md(notes_folder):
    '''
    递归合并notes_folder中的所有md文件，合并后文件保存为merged.md
    merge all md files in notes_folder, and
    save the merged file as '/notes_folder/merged.md'
    '''
    contents = []
    contents = merge_md_helper(notes_folder, contents)
    merged_note_path = os.path.join(notes_folder, 'merged.md')
    with open(merged_note_path, 'a', encoding='utf-8') as f:
        f.writelines(contents)
    print('\nMerge md files done.')  # 显示处理进度

def set_blank_lines(note, num=1):
    '''
    设置两段之间的空行数，默认为空一行
    set the number of blank lines between two paragraphs
    '''
    with open(note, 'r', encoding='utf-8') as f:
        text = f.readlines()
    
    new_text = ''
    for line in text:
        if line.split():  # 非空行
            new_text += line.strip() + '\n' * (num + 1)

    with open(note, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Set blank lines done.')

def decrease_hd_level(note, num=1):
    '''
    所有标题降低num级
    decrease all heading levels by num
    '''
    with open(note, 'r', encoding='utf-8') as f:
        text = f.readlines()

    new_text = ''
    for line in text:
        if re.search(r'^#+\s', line):  # 以一个或多个#开头的标题
            line = '#' * num + line.strip() + '\n'
        new_text += line

    with open(note, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f'Decrease heading levels by {num} done.')


def increase_hd_level(note, num=1):
    '''
    所有层级大于num的标题增加num级
    increase all heading levels (higher than num level) by num
    ''' 
    with open(note, 'r', encoding='utf-8') as f:
        text = f.readlines()

    new_text = ''
    for line in text:
        if re.search(r'^#{' + str(num + 1) + ',}\s', line): # 以至少2个#开头的标题
            line = line[num:].strip() + '\n'
        new_text += line

    with open(note, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f'Increase heading levels by {num} done.')


def format_on2md(note):
    '''
    format the text with following rules:
        1月 → # 1月\n\n
        1.1 → ## 1.1\n\n
        正文 → 正文\n\n
        2021年1月1日 → delete
        23:10 → delete
        空行 → delete
    '''

    with open(note, 'r', encoding='utf-8') as f:
        text = f.readlines()

    # 正则表达式
    p1 = re.compile(r'^\s*\w*月\s*$')  # XX月 → # XX月\n\n
    p2 = re.compile(r'^\s*\d{1,2}\.\d{1,2}\s*$')  # 1.1 → ## 1.1\n\n
    p3 = re.compile(r'[\u4E00-\u9FA5\w]+')  # 正文 → 正文\n\n # 这个也会匹配2021年1月1日，p4要在p3前面
    p4 = re.compile(r'^\d{4}年\d{1,2}月\d{1,2}日$')  # 2021年1月1日 → delete
    p5 = re.compile(r'^\d{1,2}:\d{1,2}$')  # 23:10 → delete

    new_text = ''
    for line in text:
        if p4.search(line) or p5.search(line):
            line = ''
        elif p1.search(line):
            line = '# ' + line.strip() + '\n\n'  # 需要两个换行符
        elif p2.search(line):
            line = '## ' + line.strip() + '\n\n'
        elif p3.search(line):
            line = line.strip() + '\n\n'
        elif not line.split():  # 匹配换行
            line = ''
        new_text += line

    with open(note, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Format on2md done.')
