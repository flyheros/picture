import os
import pandas as pd
import streamlit as st
from datetime import datetime
from pathlib import Path
from PIL import Image
import base64
import io

st.set_page_config (layout='wide')

# 폴더의 파일 및 폴더 정보를 얻는 함수
def get_folder_file_info(folder_path):
    file_info_list = []
    
    # 모든 하위 폴더까지 순회하며 파일 및 폴더 정보 수집
    for root, dirs, files in os.walk(folder_path):
        # 폴더 정보 추가
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            modification_time = os.path.getmtime(dir_path)
            mod_time_str = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
            
            file_info_list.append({
                "Name": f"📁 {dir_name}",
                "Type": "Folder",
                "Modification Date": mod_time_str,
                "Size (bytes)": "-",
                "Path": dir_path
            })
        
        # 파일 정보 추가
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            modification_time = os.path.getmtime(file_path)
            mod_time_str = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
            
            file_info_list.append({
                "Name": file,
                "Type": "File",
                "Modification Date": mod_time_str,
                "Size (bytes)": file_size,
                "Path": file_path
            })
    
    # DataFrame으로 변환
    return pd.DataFrame(file_info_list).sort_values('Path')


def get_folder_file_info2(folder_path):
    file_info_list = []
    
    # 모든 하위 폴더까지 순회하며 파일 및 폴더 정보 수집
    for root, dirs, files in os.walk(folder_path):
        # 폴더 정보 추가
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            modification_time = os.path.getmtime(dir_path)
            mod_time_str = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
            
            file_info_list.append({
                "Name": f"📁 {dir_name}",
                "Type": "Folder",
                "Modification Date": mod_time_str,
                "Size (bytes)": "-",
                "Path": dir_path,
                "썸네일": None  # 폴더는 썸네일이 필요 없으므로 None
            })
        
        # 파일 정보 추가
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            modification_time = os.path.getmtime(file_path)
            mod_time_str = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')

            # 이미지 파일인 경우 썸네일 생성
            thumbnail = None
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  # 이미지 파일 확장자 확인
                try:
                    with Image.open(file_path) as img:
                        img.thumbnail((50, 50))  # 썸네일 크기 조정

                        # Base64로 변환
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        thumbnail = f'<img src="data:image/png;base64,{img_str}" width="50" height="50"/>'
                except Exception as e:
                    print(f"썸네일 생성 실패: {e}")

            file_info_list.append({
                "Name": file,
                "Type": "File",
                "Modification Date": mod_time_str,
                "Size (bytes)": file_size,
                "Path": file_path,
                "썸네일": thumbnail  # 이미지일 경우 썸네일 포함
            })
    
    # DataFrame으로 변환
    return pd.DataFrame(file_info_list).sort_values('Path')


def get_files_info(uploaded_files):
    file_data=[]
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_size = uploaded_file.size / (1024 * 1024)  # MB 단위
        file_mod_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 업로드된 파일은 현재 시점을 수정 날짜로 설정
        # file_data.append({"파일명": file_name, "수정한 날짜": file_mod_time, "용량(MB)": round(file_size, 2)})
        
        # 이미지 파일 여부 확인
        if uploaded_file.type.startswith('image/'):
            image = Image.open(uploaded_file)
            
            image = Image.open(uploaded_file)
            image.thumbnail((30, 30))

            # Base64로 변환
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            img_html = f'<img src="{img_str}" width="30" height="30"/>'
            
            # 파일 데이터에 정보 추가
            file_data.append({
                "파일명": file_name,
                "수정한 날짜": file_mod_time,
                "용량(MB)": round(file_size, 2),
                "썸네일":  f'<img src="data:image/png;base64,{img_str}" width="30" height="30"/>'
            })
        else:
            # 이미지가 아닐 경우 썸네일 없이 데이터 추가
            file_data.append({
                "파일명": file_name,
                "수정한 날짜": file_mod_time,
                "용량(MB)": round(file_size, 2),
                "썸네일": None
            })
    
    return file_data
# -----------------------------------------------------------------------------
uploaded_files=""
with st.sidebar:
    tab_folder = st.tabs(["폴더 입력", "파일 선택"])
    with tab_folder[0]:
        folder_path = st.text_input("폴더 경로를 입력하세요", r"C:\Users\User\Pictures\20~30세(12장)")
        btn_folder= st.button("조회")
        
    with tab_folder[1]: 
        # 파일 업로더로 파일 선택 (다중 선택 가능)
        uploaded_files = st.file_uploader("파일을 선택하세요", accept_multiple_files=True)

# 파일이 선택된 경우 파일 정보를 데이터프레임에 담기
if uploaded_files:
    file_data = get_files_info(uploaded_files)   

    # 데이터프레임으로 변환 후 메인 화면에 표시
    df = pd.DataFrame(file_data)
    # DataFrame의 썸네일을 HTML로 표시
    df['썸네일'] = df['썸네일'].apply(lambda x: x if x is not None else '')
    
    # Streamlit의 markdown을 사용하여 HTML 출력
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # CSS 스타일 추가
    st.markdown(
        """
        <style>
        .thumbnail:hover {
            transform: scale(5);  /* 확대 비율 */
            z-index: 999;  /* 다른 요소 위에 놓이도록 */
            transition: transform 0.2s;  /* 부드러운 전환 효과 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if btn_folder:
    if os.path.isdir(folder_path):
        # 폴더가 유효하면 파일 및 폴더 정보를 가져옴
        file_data = get_folder_file_info2(folder_path)

        
        df = pd.DataFrame(file_data)
        # DataFrame의 썸네일을 HTML로 표시
        df['썸네일'] = df['썸네일'].apply(lambda x: x if x is not None else '')
        
        # Streamlit의 markdown을 사용하여 HTML 출력
        st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

        # CSS 스타일 추가
        st.markdown(
            """
            <style>
            .thumbnail:hover {
                transform: scale(5);  /* 확대 비율 */
                z-index: 999;  /* 다른 요소 위에 놓이도록 */
                transition: transform 0.2s;  /* 부드러운 전환 효과 */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        st.dataframe(df, use_container_width=True)
        
        


        
        
    else:
        st.error("유효한 폴더 경로를 입력하세요.")