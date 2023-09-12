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

from PotentialFiles import PotentialFiles
from PIL import Image

platform_info=""

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

def getAllFiles():
    file_types=[]
    file_objects=[]
    file_paths=[]
    folder_path=pathlib.Path("题目1：富文本敏感信息泄露检测/赛题材料/")

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

def readFileTo(Format,Path,OCR=False,AK=False,OFFICE=False,WPS=False,TXTLike=False,PDF=False):
    content=""
    if(OCR==True):
        file_path=pathlib.Path(Path)
        content=pytesseract.image_to_string(Image.open(file_path))
    elif(AK==True):
        pass
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
        if(Format=="" or Format=="TXT"):
            with open(Path,"r") as file:
                content=file.readlines()
        if(Format=="YML"):
            with open(Path,"r") as file:
                content=yaml.safe_load(file)
        if(Format=="XML"):
            temp_string=[]
            xml_tree=xml.etree.ElementTree.prase(Path)
            for element in xml_tree:
                temp_string.append(element.get("name"))
                temp_string.append(element.get("value"))
            content="".join(temp_string)             
        if(Format=="PROPERTIES"):
            pass
    elif(PDF==True):
        pdf_reader=pypdf.PdfReader(Path)
        for page in pdf_reader.pages:
            content=page.extract_text()

    return content

def convertToPDF(Path,Original):
    if(platform_info=="Windows"):
        if(Original=="DOCX"):
            docx2pdf.convert(Path)
        elif(Original=="DOC"):
            pass

def extract(Path):
    zip_files=[]
    for roots,dirs,files in os.walk(Path):
        for file in files:
            if os.path.splitext(file)[1].endswith(".zip"):
                zip_files.append(os.path.join(roots, file).replace("\\","/"))
    for file in zip_files:  
        file_path=pathlib.Path(file)
        zip_file=zipfile.ZipFile(file_path)
        zip_file.extractall(file_path.parent.resolve())
        
# Debug使用---------------非功能性代码
print(getAllDisk())
for objects in getAllFiles():
    if objects.file_type=="DOC":
        for path in objects.path:
            readFileTo("DOC",path,OFFICE=True)
        