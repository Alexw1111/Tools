import argparse  
import os  
import py7zr  
import rarfile  
from tqdm import tqdm  
  
# 定义解压函数，包含进度条  
def extract_with_progress(input_path, output_path, archive_type):  
    if archive_type == '7z':  
        with py7zr.SevenZipFile(input_path, mode='r') as archive:  
            all_files = archive.getnames()  
            for file_name in tqdm(all_files, desc="解压进度", ncols=100):  
                # Modified line below to ensure 'path' is passed correctly  
                archive.extract(file_name, output_path)  # Removed the 'path=' keyword  
    elif archive_type == 'rar':  
        # RAR extraction remains the same  
        with rarfile.RarFile(input_path) as archive:  
            all_files = archive.namelist()  
            for file_name in tqdm(all_files, desc="解压进度", ncols=100):  
                archive.extract(file_name, output_path)  
    else:  
        print(f"不支持的压缩格式: {archive_type}") 
  
def main():  
    parser = argparse.ArgumentParser(description='解压.7z或.rar文件')  
    parser.add_argument('input_path', type=str, help='压缩文件的路径')  
    parser.add_argument('output_path', type=str, help='解压到的目标路径')  
    args = parser.parse_args()  
  
    # 判断文件是否存在  
    if not os.path.isfile(args.input_path):  
        print(f"文件不存在：{args.input_path}")  
        return  
  
    # 获取压缩文件类型  
    file_extension = os.path.splitext(args.input_path)[1][1:].lower()  # 去掉点号并转为小写  
  
    # 确保输出目录存在  
    if not os.path.exists(args.output_path):  
        os.makedirs(args.output_path)  
  
    # 解压文件并显示进度  
    if file_extension in ('7z', 'rar'):  
        extract_with_progress(args.input_path, args.output_path, file_extension)  
    else:  
        print(f"不支持的文件格式：.{file_extension}")  
  
if __name__ == "__main__":  
    main()
