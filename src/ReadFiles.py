import platform
import psutil
import os
import pathlib
import pytesseract
import zipfile
import pypdf
import yaml
import xml.etree.ElementTree as ET
import email
import hivex
from Registry import Registry
from PotentialFiles import PotentialFiles
from PIL import Image

platform_info = ""


# Read all drive letters of the target host
def getAllDisk():
    global platform_info
    platform_info = platform.system()
    if platform_info == "Windows":
        print("Windows")
        return psutil.disk_partitions()
    elif platform_info == "Linux":
        print("Linux")
        return psutil.disk_partitions()
    else:
        print(platform_info)
        return psutil.disk_partitions()


# Read all files under the path (disk) and save their path and format as a file object
# Save different file objects into the object array file_objects
def getAllFiles(Disk):
    file_types = []
    file_objects = []
    file_paths = []
    folder_path = pathlib.Path(Disk)

    readAttach(folder_path)
    extract(folder_path)

    for roots, dirs, files in os.walk(folder_path):
        for file in files:
            if os.path.splitext(file)[1].endswith(".zip"):
                continue
            else:
                file_types.append(os.path.splitext(file)[1])
                # Get the full path of the file
                file_paths.append(os.path.join(roots, file).replace("\\", "/"))

    file_types = list(set(file_types))

    for format_type in file_types:
        file_type_path = []
        file_type_path.clear()
        for path in file_paths:
            if format_type != "" and path.endswith(format_type):
                file_type_path.append(path)
            elif format_type == "" and pathlib.Path(path).suffix == "":
                file_type_path.append(path)
        file_objects.append(
            PotentialFiles(format_type.upper().strip("."), file_type_path)
        )

    return file_objects


# Read the file content and return it as String
def readFileTo(Format, Path, OCR=False, DECODE=False, TXTLike=False, PDF=False):
    content = ""

    if OCR == True:
        file_path = pathlib.Path(Path)
        content = pytesseract.image_to_string(Image.open(file_path))

    elif DECODE == True:
        if Format == "HIV":
            h = hivex.Hivex(Path, verbose=False)
            print(h)
        elif Format == "PUB":
            pass
        elif Format == "EML":
            with open(Path, "rb") as eml:
                message = email.message_from_binary_file(eml)
            temp_string = []
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_type() == "text/html":
                        temp_string.append(part.get_payload(decode=True).decode())
                    else:
                        continue
            else:
                temp_string.append(message.get_payload(decode=True).decode())
            content = "".join(temp_string)

    elif TXTLike == True:
        if Format == "TXT":
            with open(Path, "r") as file:
                content = file.readlines()
        elif Format == "YML":
            with open(Path, "r") as file:
                content = yaml.safe_load(file)
        elif Format == "XML":
            temp_string = []
            xml_tree = ET.parse(Path)
            for element in xml_tree.findall(".//"):
                temp_string.append(element.get("name"))
                temp_string.append(element.get("value"))
            content = "".join(temp_string)
        elif Format == "PROPERTIES":
            with open(Path, "r") as file:
                content = file.readlines()
        elif Format == "":
            path_string = str(Path)
            if path_string.endswith("token"):
                with open(Path, "r") as file:
                    content = file.readlines()
            elif path_string.endswith("authorized_keys"):
                with open(Path, "r") as file:
                    content = file.readlines()
            elif path_string.endswith("sam"):
                temp_string = []
                reg = Registry.Registry(Path)
                key = reg.open("SAM\\Domains\\Account\\Users")
                for subkey in key.subkeys():
                    temp_string.append("Username: " + subkey.name() + " ")
                content = "".join(temp_string)
        else:
            with open(Path, "r") as file:
                content = file.readlines()

    elif PDF == True:
        temp_string = []
        pdf_reader = pypdf.PdfReader(Path)
        for page in pdf_reader.pages:
            temp_string.append(page.extract_text())
        content = "".join(temp_string)
    return content.__str__()


# Extract all ZIP files
def extract(Path):
    zip_files = []
    # Traverse
    for roots, dirs, files in os.walk(Path):
        for file in files:
            if os.path.splitext(file)[1].endswith(".zip"):
                zip_files.append(os.path.join(roots, file).replace("\\", "/"))
    # Extract
    for file in zip_files:
        file_path = pathlib.Path(file)
        zip_file = zipfile.ZipFile(file_path)
        zip_file.extractall(file_path.parent.resolve())


# Read attachments of EML files
def readAttach(Path):
    email_files = []  # Path to store all EML files
    temp_byte_filename = (
        []
    )  # Storing the file name in bytes (the file name may be incomplete)
    temp_str_filename = []  # The file name in byte format is decoded into String
    temp_encode_format = ""  # Encoding format

    # Traverse
    for roots, dirs, files in os.walk(Path):
        for file in files:
            if os.path.splitext(file)[1].endswith(".eml"):
                email_files.append(os.path.join(roots, file).replace("\\", "/"))

    for file in email_files:
        with open(file, "rb") as eml:
            message = email.message_from_binary_file(eml)

        # Determine whether the EML content is multi-paragraph content
        if message.is_multipart():
            for part in message.walk():
                if part.get_filename():
                    for name, encoding in email.header.decode_header(
                        part.get_filename()
                    ):
                        temp_byte_filename.append(name)
                        if encoding != None:
                            temp_encode_format = encoding
                    for byte in temp_byte_filename:
                        temp_str_filename.append(byte.decode(temp_encode_format))
                    filename = "".join(temp_str_filename)
                    attachment = pathlib.Path(Path).parent.resolve().__str__()
                    with open(attachment + "/" + filename, "wb") as file:
                        file.write(part.get_payload(decode=True))
        else:
            if message.get_filename():
                for name, encoding in email.header.decode_header(
                    message.get_filename()
                ):
                    temp_byte_filename.append(name)
                    if encoding != None:
                        temp_encode_format = encoding

                for byte in temp_byte_filename:
                    temp_str_filename.append(byte.decode(temp_encode_format))

                filename = "".join(temp_str_filename)
                attachment = pathlib.Path(Path).parent.resolve().__str__()

                with open(attachment + "/" + filename, "wb") as file:
                    file.write(part.get_payload(decode=True))


getAllDisk();
readFileTo(Format='HIV', Path='D:\PythonFile\AutoAnalyse\富文本敏感信息\赛题材料\windwos\sam.hiv', TXTLike=True)