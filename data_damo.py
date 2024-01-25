import streamlit as st
import json
import os

def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            json_object = json.loads(line)
            data.append(json_object)
    return data

# Move st.set_page_config to the beginning
st.set_page_config(layout="wide")

def main():
    st.title("展示MS_Agent_Bench数据集")

    # 选择你的 JSONL 文件
    uploaded_file = st.file_uploader("上传 JSONL 文件", type=["jsonl"])

    if uploaded_file is not None:
        # 保存上传的文件到本地临时文件
        temp_file_path = "temp.jsonl"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_file.getvalue())

        st.info("文件已上传!")

        # 读取 JSONL 文件
        data = read_jsonl(temp_file_path)

        # 显示数据
        st.write("展示 JSONL 数据:")
        st.write(data)

        # 使用栅格布局显示数据表格
        cols = st.columns(2)
        with cols[0]:
            st.write(f"{0}th-{len(data)//2}th数据:")
            st.write(data[:len(data)//2])

        with cols[1]:
            st.write(f"{len(data)//2+1}th-{len(data)}th数据:")
            st.write(data[len(data)//2:])

        # 删除临时文件
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()
