import platform
import psutil
import os
import pathlib
import pytesseract
import zipfile
import pypdf
import pandas
import docx2pdf
import yaml
import xml
import email
import io

from PotentialFiles import PotentialFiles
from PIL import Image

platform_info=""

#读取目标主机的所有盘符
def getAllDisk():
    global platform_info
    platform_info=platform.system()
    if(platform_info=="Windows"):
        print("Windows")
        return psutil.disk_partitions()
    elif(platform_info=="Linux"):
        print("Linux")
        return psutil.disk_partitions()
    else:
        print(platform_info)
        return psutil.disk_partitions()

#读取路径（磁盘）下的所有文件，保存其路径和格式为一个文件对象
#将不同的文件对象存至对象数组file_objects
def getAllFiles(Disk):
    file_types=[]
    file_objects=[]
    file_paths=[]
    folder_path=pathlib.Path(Disk)

    readAttach(folder_path)
    extract(folder_path)

    for roots, dirs, files in os.walk(folder_path):
        for file in files:
            if os.path.splitext(file)[1].endswith(".zip"):
                continue
            else:
                file_types.append(os.path.splitext(file)[1])
                # 获取文件的完整路径
                file_paths.append(os.path.join(roots, file).replace("\\","/"))

    file_types=list(set(file_types))

    for format_type in file_types:
        file_type_path=[]
        file_type_path.clear()
        for path in file_paths:
            if(format_type!="" and path.endswith(format_type)):
                file_type_path.append(path)
            elif(format_type=="" and pathlib.Path(path).suffix==""):
                file_type_path.append(path)
        file_objects.append(PotentialFiles(format_type.upper().strip('.'),file_type_path))

    return file_objects

#读取文件内容，返回为String
def readFileTo(Format,Path,OCR=False,DECODE=False,OFFICE=False,WPS=False,TXTLike=False,PDF=False):
    content=""

    if(OCR==True):
        file_path=pathlib.Path(Path)
        content=pytesseract.image_to_string(Image.open(file_path))
        
    elif(DECODE==True):
        if(Format=="HIV"):
            pass
        elif(Format=="PUB"):
            pass
        elif(Format=="EML"):
            with open(Path,"rb") as eml:
                message=email.message_from_binary_file(eml)
            temp_string=[]
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_type()=="text/html":
                        temp_string.append(part.get_payload(decode=True).decode())
                    else:
                        continue
            else:
                temp_string.append(message.get_payload(decode=True).decode())
            content="".join(temp_string)

    elif(OFFICE==True):
        if(Format=="PTTX" or Format=="PPT"):
            pass
        elif(Format=="DOCX" or Format=="DOC"):
            convertToPDF(Path,Format)
        elif(Format=="XLSX" or Format=="XLS"):
            xlsx_file=pandas.ExcelFile(Path)
            sheets=xlsx_file.sheet_names
            content=pandas.read_excel(Path,sheets)
    elif(WPS==True):
        if(Format=="WPS"):
            pass
        elif(Format=="ET"):
            pass
        elif(Format=="DPS"):
            pass
    elif(TXTLike==True):
        if(Format=="TXT"):
            with open(Path,"r") as file:
                content=file.readlines()
        elif(Format=="YML"):
            with open(Path,"r") as file:
                content=yaml.safe_load(file)
        elif(Format=="XML"):
            temp_string=[]
            xml_tree=xml.etree.ElementTree.prase(Path)
            for element in xml_tree:
                temp_string.append(element.get("name"))
                temp_string.append(element.get("value"))
            content="".join(temp_string)             
        elif(Format=="PROPERTIES"):
            with open(Path,"r") as file:
                content=file.readlines()
        elif(Format==""):
            path_string=str(Path)
            if path_string.endswith("token"):
                with open(Path,"r") as file:
                    content=file.readlines()
            elif path_string.endswith("authorized_keys"):
                with open(Path,"r") as file:
                    content=file.readlines()
            elif path_string.endswith("sam"):
                pass
            elif path_string.endswith("system"):
                pass
            else:
                with open(Path,"r") as file:
                    content=file.readlines()
        else:
            with open(Path,"r") as file:
                    content=file.readlines()
    elif(PDF==True):
        temp_string=[]
        pdf_reader=pypdf.PdfReader(Path)
        for page in pdf_reader.pages:
            temp_string.append(page.extract_text())
        content="".join(temp_string)
    return content

def convertToPDF(Path,Original):
    if(platform_info=="Windows"):
        if(Original=="DOCX"):
            docx2pdf.convert(Path)
        elif(Original=="DOC"):
            pass

#解压所有ZIP文件
def extract(Path):
    zip_files=[]
    #编历
    for roots,dirs,files in os.walk(Path):
        for file in files:
            if os.path.splitext(file)[1].endswith(".zip"):
                zip_files.append(os.path.join(roots, file).replace("\\","/"))
    #解压
    for file in zip_files:  
        file_path=pathlib.Path(file)
        zip_file=zipfile.ZipFile(file_path)
        zip_file.extractall(file_path.parent.resolve())

#读取EML文件的附件
def readAttach(Path):
    email_files=[]   #存放所有EML文件的路径
    temp_byte_filename=[]  #以字节方式存放文件名（文件名可能不完整）
    temp_str_filename=[]   #字节格式的文件名解码为String
    temp_encode_format=""  #编码格式

    #编历所有文件
    for roots,dirs,files in os.walk(Path):
        for file in files:
            if os.path.splitext(file)[1].endswith(".eml"):
                email_files.append(os.path.join(roots, file).replace("\\","/"))
    
    for file in email_files:
        with open(file,"rb") as eml:
            message=email.message_from_binary_file(eml)

        #判断EML内容是否为多段内容
        if message.is_multipart():
            for part in message.walk():
                if part.get_filename():
                    for name, encoding in email.header.decode_header(part.get_filename()):
                        temp_byte_filename.append(name)
                        if encoding!=None:
                            temp_encode_format=encoding
                    for byte in temp_byte_filename:
                        temp_str_filename.append(byte.decode(temp_encode_format))
                    filename="".join(temp_str_filename)
                    attachment=pathlib.Path(Path).parent.resolve().__str__()
                    with open(attachment+"/"+filename,"wb") as file:
                        file.write(part.get_payload(decode=True))
        else:
            if message.get_filename():
                for name, encoding in email.header.decode_header(message.get_filename()):
                    temp_byte_filename.append(name)
                    if encoding!=None:
                        temp_encode_format=encoding

                for byte in temp_byte_filename:
                    temp_str_filename.append(byte.decode(temp_encode_format))
                
                filename="".join(temp_str_filename)
                attachment=pathlib.Path(Path).parent.resolve().__str__()

                with open(attachment+"/"+filename,"wb") as file:
                    file.write(part.get_payload(decode=True))

            
