import os
import pathlib
import pytesseract
import pypdf
from PotentialFiles import PotentialFiles
from PIL import Image


def getAllDisk():

    file_types=[]
    file_objects=[]
    file_paths=[]
    folder_path=pathlib.Path("题目1：富文本敏感信息泄露检测/赛题材料/")

    for roots, dirs, files in os.walk(folder_path):
        for file in files:
            file_types.append(os.path.splitext(file)[1])
            # 获取文件的完整路径
            file_paths.append(os.path.join(roots, file))

    file_types=list(set(file_types))

    for type in file_types:
        file_type_path=[]
        file_type_path.clear()
        for path in file_paths:
            if(type!="" and path.endswith(type)):
                file_type_path.append(path)
            elif(type=="" and pathlib.Path(path).suffix==""):
                file_type_path.append(path)
        file_objects.append(PotentialFiles(type.upper().strip('.'),file_type_path))

    for objects in file_objects:
        pass

def readFileTo(Format,Path,OCR=False,AK=False,OFFICE=False,WPS=False,TXTLike=False):
    file_path=pathlib.Path(Path)
    if(OCR==True):
        result=pytesseract.image_to_string(Image.open(file_path))
        print(result)
    elif(AK==True):
        pass
    elif(OFFICE==True):
        pass
    elif(TXTLike==True):
        if(Format=="PDF"):
            pdfReader=pypdf.PdfReader(Path)
            for page in pdfReader.pages:
                text=page.extract_text()
                print(text)
        elif(Format=="" or Format=="TXT"):
            with open(Path,"r") as file:
                text=file.readlines()

# readFileTo("jpg","题目1：富文本敏感信息泄露检测/赛题材料/carbon.jpg",OCR=True)
# readFileTo("PDF","题目1：富文本敏感信息泄露检测/赛题材料/add.pdf",TXTLike=True)
getAllDisk()

