# useful Functions for handling Files and Folders

import os, shutil


def list_files(folder):
    """
    递归列出folder下所有文件
    """
    files = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            files.extend(list_files(path))
        if os.path.isfile(path):
            files.append(path)
    return files


def clear_folder(folder):
    """
    if folder exists, clear it
    if folder not exists, create it
    """
    shutil.rmtree(folder, ignore_errors=True)  # 清空目标文件夹，包括文件夹本身
    if not os.path.exists(folder):
        os.makedirs(folder)
