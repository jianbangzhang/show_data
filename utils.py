import json
import streamlit as st

def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            json_object = json.loads(line)
            data.append(json_object)
    return data


def choose_dataset(default_file):
    upload_option = st.radio("选择数据源", ["上传jsonl文件", "加载默认文件"])
    file=None
    if upload_option == "上传jsonl文件":
        # 选择上传的 JSONL 文件
        uploaded_file = st.file_uploader("上传 JSONL 文件", type=["jsonl"])
        if uploaded_file is not None:
            file=uploaded_file
    elif upload_option == "加载默认文件":
        file=default_file
    else:
        raise NotImplementedError
    return file

