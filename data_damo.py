import streamlit as st
import os
from utils import read_jsonl





def show_data(file):
    # 保存上传的文件到本地临时文件
    if isinstance(file, str):
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



def show(default_file_path):
    show_data(default_file_path)

