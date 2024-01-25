import streamlit as st
import pandas as pd
import json
import os

def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            json_object = json.loads(line)
            data.append(json_object)
    return data

def show_data(file):
    # 保存上传的文件到本地临时文件
    if isinstance(file,str):
        temp_file_path = file
    else:
        temp_file_path = "temp.jsonl"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file.getvalue())

    st.success("正在拼命加载文件.............................")

    # 读取 JSONL 文件
    data = read_jsonl(temp_file_path)

    # 显示数据
    st.write("展示 JSONL 数据:")
    st.write(data)

    # 使用栅格布局显示数据表格
    cols = st.columns(2)
    with cols[0]:
        st.write(f"{1}th-{len(data) // 2}th数据:")
        st.write(data[:len(data) // 2])

    with cols[1]:
        st.write(f"{len(data) // 2 + 1}th-{len(data)}th数据:")
        st.write(data[len(data) // 2:])

    # 删除临时文件
    os.remove(temp_file_path)


def main():
    st.title("展示MS-Agent-Bench数据集")

    # 选择上传文件或加载默认文件
    upload_option = st.radio("选择数据源", ["上传jsonl文件", "加载默认文件"])

    if upload_option == "上传jsonl文件":
        # 选择上传的 JSONL 文件
        uploaded_file = st.file_uploader("上传 JSONL 文件", type=["jsonl"])
        if uploaded_file is not None:
           show_data(uploaded_file)
    elif upload_option == "加载默认文件":
        # 加载默认 JSONL 文件
        default_file_path = "dev.jsonl"
        show_data(default_file_path)
    else:
        raise NotImplementedError

if __name__ == "__main__":
    main()
