import streamlit as st
import os
from data_damo import show
from data_descript import describe_data
from data_process import get_ms_tool_dataset_test,get_ms_tool_dataset_train
from utils import choose_dataset


cur_path = os.path.dirname(os.path.abspath(__file__))
default_file_path = os.path.join(cur_path, "dev.jsonl")
st.set_page_config(layout="wide")

def main():
    st.title("MS-Agent-Bench数据集")
    file=choose_dataset(default_file_path)
    navigation = st.radio("数据集", ["选择本地文件或上传文件","数据展示", "数据说明","数据预处理"])
    if navigation == "选择本地文件或上传文件":
        st.title("文件选择：")
        st.write("请选择您的文件...")

    elif navigation == "数据展示":
        st.title("数据集展示")
        show(default_file_path)

    elif navigation == "数据说明":
        st.title("数据集说明")
        data_string,data_detail,data_note=describe_data()
        st.write(data_string)
        st.write(data_detail)
        st.write(data_note)

    elif navigation == "数据预处理":
        st.title("数据集预处理")
        st.write("if flag = 1, the token should be origin result, if 0, it should be ignored")
        data_id = st.text_input("输入数据的ID:")

        if data_id:
            data_id=int(data_id)
        else:
            data_id=1

        if file is not None:
            raw_data,post_data=get_ms_tool_dataset_train(file,data_id)
            st.write(f"{int(data_id)}th原始数据:")
            st.write(raw_data)
            st.write(f"{int(data_id)}th处理后数据:")
            st.write(post_data)
            st.write("测试阶段数据处理......")
            test_data=get_ms_tool_dataset_test(file)
            st.write(test_data)
        else:
            st.write("请先选择上传文件............")
    else:
        pass

if __name__ == "__main__":
    main()
