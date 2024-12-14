import os
import shutil
import csv
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import sys
import re




def create_folder(rootFolder):
    # 1. 폴더 생성
    # rootFolder="D:\\사진"
    folders = [ "small", "분류", "분류_예외"]
    for folder in folders:
        if not os.path.exists(rootFolder + "\\" + folder):
            os.makedirs(rootFolder + "\\" + folder)

def get_image_date(file_path):
    try:
        # Pillow의 이미지 크기 제한을 늘림
        Image.MAX_IMAGE_PIXELS = None
        image = Image.open(file_path)
        # GIF 파일이 아닌 경우에만 이미지 정보 가져오기
        if image.format != 'GIF':
            exif_data = image._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    if TAGS.get(tag) == 'DateTimeOriginal':
                        return datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Error retrieving image date: {e}")
        return e


def get_file_dates(file_path):
    try:
        created_at = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        updated_at = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        return created_at, updated_at
    except Exception as e:
        print(f"Error retrieving file dates: {e}")
        return e, None

def resize_image(input_path, output_path, scale=0.3):
    try:
        image = Image.open(input_path)
        new_size = (int(image.width * scale), int(image.height * scale))
        resized_image = image.resize(new_size)
        resized_image.save(output_path)
    except Exception as e:
        print(f"Error resizing image: {e}")

def extract_date_from_filename(filename):
    # 문자열에서 숫자 부분만 추출
    numbers = re.findall(r'\d+', filename)
    
    # 추출된 숫자가 6개 이상인 경우 YYYYMMDD 형식으로 변환하여 반환
    if len(numbers) >= 3:
        year = numbers[0]
        month = numbers[1]
        day = numbers[2]
        return f"{year}{month.zfill(2)}{day.zfill(2)}"
    else:
        return None


def get_file_size(file_path):
    try:
        file_size = os.path.getsize(file_path)
        return file_size
    except Exception as e:
        print(f"Error retrieving file size: {e}")
        return None


def write_csv(file_path, rootFolder):
    # CSV 파일 생성 및 초기화
    csv_file_path = rootFolder + "\\결과.csv"
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['folder', 'filename', '확장자', 'file_size', 'pictured_at', 'created_at', 'updated_at', 'new_folder', 'small_folder_YYYYMMDD', 'folder_YYYYMMDD', 'result'])

    # 2. 파일 처리

    for root, _, files in os.walk(rootFolder + "\\원본"):
        for org_filename in sorted(files):
            try:
                file_path = os.path.join(root, org_filename)
                file_size = get_file_size(file_path)
                folder = os.path.dirname(file_path)
                YYYYMMDD = extract_date_from_filename(org_filename)
                pictured_at = get_image_date(file_path) if org_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) else None
                created_at, updated_at = get_file_dates(file_path)
                result = "Success"

                if org_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    date_candidates = [datetime.datetime.strptime(YYYYMMDD, '%Y%m%d') if YYYYMMDD else None, pictured_at, created_at, updated_at]
                    date_candidates = [date for date in date_candidates if date]
                    folder_YYYYMMDD = min(date_candidates).strftime('%Y%m%d') if date_candidates else 'Unknown'
                    new_folder = os.path.join(rootFolder + "\\분류", folder_YYYYMMDD[:6])
                    new_file_name=''
                else:
                    date_candidates = [datetime.datetime.strptime(YYYYMMDD, '%Y%m%d') if YYYYMMDD else None, created_at, updated_at]
                    date_candidates = [date for date in date_candidates if date]
                    folder_YYYYMMDD = min(date_candidates).strftime('%Y%m%d') if date_candidates else 'Unknown'
                    new_folder = rootFolder + "\\분류_예외"
                    
                
                filename=  folder_YYYYMMDD+ '_' + org_filename    
                new_file_name = os.path.join(new_folder, filename)


                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)
                shutil.copy2(file_path, new_file_name)

                if org_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    small_folder = os.path.join(rootFolder + "\\small", folder_YYYYMMDD[:6])
                    if not os.path.exists(small_folder):
                        os.makedirs(small_folder)
                    small_file_path = os.path.join(small_folder, 'small_' + filename)
                    resize_image(file_path, small_file_path)

            except Exception as e:
                result = f"Error: {e}"

            # CSV 파일에 로그 저장
            with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([folder, org_filename, org_filename.split(".")[1], file_size, pictured_at, created_at, updated_at, folder_YYYYMMDD, small_file_path, new_file_name, result])

    print("작업 완료")
