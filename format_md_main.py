# 对md文件进行一些格式转换工作

import os, shutil
import utils.format_md as fmd
import utils.dirs as dirs
import utils.on2ob as on2ob

if __name__ == '__main__':
    '''
    对md文件进行一些格式转换工作
    '''
    # 初始化notes文件夹
    old_notes_folder = os.path.join(os.getcwd(), 'old_notes')  # 需要修改的旧md文件放这里
    new_notes_folder = os.path.join(os.getcwd(), 'new_notes')  # 修改后的新md文件在这里
    shutil.rmtree(new_notes_folder, ignore_errors=True)  # 清空目标文件夹，包括文件夹本身
    shutil.copytree(old_notes_folder, new_notes_folder)  # 复制旧文件到新文件夹，后续处理都在新文件夹中进行

    files = dirs.list_files(new_notes_folder)  # 列出文件夹下所有文件
    for note in files:
        note_name = os.path.splitext(note)[0].split('\\')[-1]
        print(f'\nWorking on file: {note_name}.md')  # 显示处理进度

        on2ob.links_on2ob(note)  # 将Onenote内链替换为Obsidian内链

        fmd.set_blank_lines(note, num=1)  # 设置段落间空若干数
        fmd.decrease_hd_level(note, num=1)  # 所有标题降低若干级
        fmd.increase_hd_level(note, num=1)  # 所有标题增加若干级
        fmd.split_md(note)  # 分割md文件
        # fmd.format_on2md(note)  # 将提取的文本内容格式化，设置一二级标题等等

    fmd.merge_md(new_notes_folder)  # 合并md文件

    print('\nAll done!')
