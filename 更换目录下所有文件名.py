import os
import re

# 定义记录文件名
RECORD_FILE = "rename_record.txt"

def rename_files():
    # 获取当前目录
    root_dir = os.getcwd()
    file_count = 0
    record_lines = []

    # 遍历当前目录及其所有子目录
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        # 跳过以"."开头的文件夹
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for filename in filenames:
            # 跳过.txt、.py和.exe文件
            if filename.endswith(('.txt', '.py', '.exe')):
                continue

            # 获取文件的完整路径
            full_path = os.path.join(dirpath, filename)

            # 生成新的文件名（数字命名）
            new_filename = f"{file_count}.rename"
            new_full_path = os.path.join(dirpath, new_filename)

            # 重命名文件
            os.rename(full_path, new_full_path)

            # 记录原文件名和新文件名
            record_lines.append(f"{full_path} -> {new_full_path}\n")
            file_count += 1

    # 将记录写入文件
    with open(RECORD_FILE, "w", encoding="utf-8") as record_file:
        record_file.writelines(record_lines)

    print(f"共重命名 {file_count} 个文件，记录已保存到 {RECORD_FILE}")


def restore_files():
    # 检查记录文件是否存在
    if not os.path.exists(RECORD_FILE):
        print(f"未找到记录文件 {RECORD_FILE}，无法还原文件名。")
        return

    # 读取记录文件
    with open(RECORD_FILE, "r", encoding="utf-8") as record_file:
        lines = record_file.readlines()

    # 遍历记录文件，还原文件名
    for line in lines:
        original_path, new_path = line.strip().split(" -> ")
        if os.path.exists(new_path):
            os.rename(new_path, original_path)
        else:
            print(f"未找到文件 {new_path}")
    # 删除记录文件
    os.remove(RECORD_FILE)
    print(f"文件名已还原，记录文件 {RECORD_FILE} 已删除。")


def main():
    if os.path.exists(RECORD_FILE):
        print(f"检测到记录文件 {RECORD_FILE}，将尝试还原文件名。")
        restore_files()
    else:
        print("未检测到记录文件，将开始重命名文件。")
        rename_files()


if __name__ == "__main__":
    main()