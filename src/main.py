import ReadFiles
import NLPProcess
import concurrent.futures
import threading


if __name__=='__main__':
    
    office_type=["DOCX","DOC","PPT","PPTX","XLS","XLSX"]
    wps_type=["WPS","ET","DPS"]
    txt_like=["TXT","PROPERTIES","YML","XML",""]
    img_class=["PNG","JPG","JPEG","BMP","ICO"]
    Disks=[disk.mountpoint for disk in ReadFiles.getAllDisk()]
    contents=[]
    print(Disks)

    file_obj=ReadFiles.getAllFiles("题目1：富文本敏感信息泄露检测/赛题材料/")
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as execute:

            for obj in file_obj:
                if obj.file_type in img_class:
                    for path in obj.path:
                        contents.append(execute.submit(ReadFiles.readFileTo,obj.file_type,path,OCR=True))
                if obj.file_type in office_type:
                    for path in obj.path:
                    #conetents=execute.submit(ReadFiles.readFileTo(obj.file_type,path,OFFICE=True))
                        pass
                if obj.file_type in txt_like:
                    for path in obj.path:
                        #contents.append(execute.submit(ReadFiles.readFileTo(obj.file_type,path,TXTLike=True)))
                        pass


            for content in concurrent.futures.as_completed(contents):
                print(f"",{content.result()})
    except TypeError as e:
        print(e)
