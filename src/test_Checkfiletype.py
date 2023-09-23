import zipfile
import os


# 解压缩文件
def unzip_file(zip_file, extract_dir):
    with zip_file.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)


# 检查文件类型
def get_file_type(file_path):
    file_extension = os.path.splitext(file_path)[-1].lower()
    if file_extension in ('.txt', '.log', '.conf'):
        return 'text'
    elif file_extension in ('.docx', '.doc'):
        return 'docx'
    elif file_extension in ('.xlsx', '.xls'):
        return 'xlsx'
    elif file_extension in ('.pptx', '.ppt'):
        return 'pptx'
