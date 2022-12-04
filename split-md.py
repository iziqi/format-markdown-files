# 分割Markdown文件：
#   按照一级标题创建文件夹，每个二级标题段落为该文件夹下的单独md文件
#   分割后的文件保存在separate_notes文件夹
# Split the given markdown file: 
#   Create different folders by top-level headings
#   Split markdown files by second-level headings
#   Seperate files will be located in 'separate_notes' folder

import re, os
import shutil

def split_md(note_to_be_splited, new_notes_folder):
    '''
    按照一级标题创建文件夹，每个二级标题段落为该文件夹下的单独md文件
    Split the given markdown file: 
    First create different folders by top-level headings
    then split markdown files by second-level headings
    '''
    # 正则表达式
    p1 = re.compile(r'^#\s.+$') # # XXXXX 一级标题
    p2 = re.compile(r'^##\s.+$') # ## XXXXX 二级标题
    p3 = re.compile(r'.', re.DOTALL) # 匹配正文和换行 匹配所有内容

    # 按照分级标题分割文件，一级标题为文件夹，二级标题段落为该文件夹下的单独md文件
    with open(note_to_be_splited,'r',encoding='utf-8') as f:
        count = 0
        for line in f: 
            if p1.search(line):
                tmp_folder_name = line[2:].replace('\n', '') # 提取一级标题作为文件夹名
                tmp_folder_path = os.path.join(new_notes_folder, tmp_folder_name)
                shutil.rmtree(tmp_folder_path, ignore_errors=True) # 清空目标文件夹，包括文件夹本身
                if not os.path.exists(tmp_folder_path): os.makedirs(tmp_folder_path)
            elif p2.search(line):
                if count != 0: # 排除第一次经过，保存上一个二级标题下的内容
                    with open(separate_note_path,'a', encoding='utf-8') as f:
                        f.write(seperate_note_text)
                count += 1
                separate_note_name = line[3:].replace('\n', '') # 提取二级标题为md文件名
                separate_note_path = os.path.join(tmp_folder_path, separate_note_name + '.md')
                seperate_note_text = '# ' + separate_note_name + '\n' # 二级标题名称作为md开头
            elif p3.search(line):
                if count != 0:
                    seperate_note_text += line
        if count != 0: # 处理文件结尾的最后一个二级标题
            with open(separate_note_path,'a', encoding='utf-8') as f:
                f.write(seperate_note_text)

# ------------------------------------------------------------------
## main
# ------------------------------------------------------------------
if __name__ == '__main__':
    '''
    按照分级标题分割文件，一级标题为文件夹，二级标题段落为该文件夹下的单独md文件
    '''
    # 初始化notes文件夹
    old_notes_folder = os.path.join(os.getcwd(), 'original_notes') # folder for old Markdown notes
    new_notes_folder = os.path.join(os.getcwd(), 'separate_notes') # folder for new Markdown notes

    # 初始化new notes文件夹
    shutil.rmtree(new_notes_folder, ignore_errors=True) # 清空目标文件夹，包括文件夹本身
    if not os.path.exists(new_notes_folder): os.makedirs(new_notes_folder)

    # split md
    for note in os.listdir(old_notes_folder):
        print(f'Working on file: {note}') # 显示处理进度

        note_name = os.path.splitext(note)[0]
        note_path = os.path.join(old_notes_folder, note)

        # 创建存放分割后notes的文件夹
        note_folder = os.path.join(new_notes_folder, note_name) # 
        shutil.rmtree(note_folder, ignore_errors=True)
        if not os.path.exists(note_folder): os.makedirs(note_folder)

        # 分割该note
        split_md(note_path, note_folder)