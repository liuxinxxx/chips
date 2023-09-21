import ReadFiles
import NLPProcess

if __name__=='__main__':
    office_type=["DOCX","DOC","PPT","PPTX","XLS","XLSX"]
    wps_type=["WPS","ET","DPS"]
    txt_like=["TXT","PROPERTIES","YML","XML",""]
    img_class=["PNG","JPG","JPEG","BMP","ICO"]
    Disks=[disk for disk in ReadFiles.getAllDisk()]
    file_obj=ReadFiles.getAllFiles("题目1：富文本敏感信息泄露检测/赛题材料/")
    for obj in file_obj:
        if obj.file_type in img_class:
            for path in obj.path:
                conetent=ReadFiles.readFileTo(obj.file_type,path,OCR=True)
                NLPProcess.analysText("en",conetent)
        