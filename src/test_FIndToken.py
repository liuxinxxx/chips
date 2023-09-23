import os


def find_and_read_token(folder_path):
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件名是否包含 "token"，您可以根据实际情况修改匹配的条件
            if "token" in file:
                token_file_path = os.path.join(root, file)
                try:
                    # 打开并读取token文件中的密钥
                    with open(token_file_path, 'r') as token_file:
                        token_key = token_file.read()
                        return token_key
                except Exception as e:
                    print(f"无法读取文件 {token_file_path}: {e}")

    # 如果未找到token文件，则返回 None 或适当的默认值
    return None

