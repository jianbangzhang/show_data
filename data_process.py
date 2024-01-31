import ast
import re
from utils import read_jsonl
import json
import os

def get_ms_tool_dataset_train(file_path:str,data_index:int) -> tuple:
    # ms_tool_dataset: for train
    # each data may contain multiple segments, they are organized as a list
    # and split by flag. 0 for user input/ tool execute result..., 1 for label


    origin_data = read_jsonl(file_path)

    all_inputs_str = []
    all_inputs_flag = []
    for i,d in enumerate(origin_data):
        if data_index!=i:
            continue
        content = d['conversations']
        if isinstance(content, str):
            content = ast.literal_eval(content)

        # ilegal data
        if len(content) == 0 or content[0]['from'] != 'system':
            continue

        system_str = '<|system|>:' + content[0]['value']

        inputs_str = [system_str]  # segment of conservations
        inputs_flag = [
            0
        ]  # a flag to indicate whether the segment is assistant response

        for i in range(len(content) // 2):
            if len(content[2 * i + 2]['value']) == 0:
                continue

            assert content[2 * i + 1]['from'] == 'user'
            assert content[2 * i + 2]['from'] == 'assistant'
            # user input
            inputs_str.append('\n\n<|user|>:' + content[2 * i + 1]['value'])
            inputs_flag.append(0)

            # assistant response
            origin_response_str = '\n\n<|assistant|>:' + content[
                2 * i + 2]['value'] + '\n\n</s>'

            idx1, idx2 = -1, 0
            iter1 = re.finditer(r'<\|startofexec\|>', origin_response_str)
            iter2 = re.finditer(r'<\|endofexec\|>', origin_response_str)

            for i1, i2 in zip(iter1, iter2):
                idx1 = i1.start()

                # llm response
                inputs_str.append(origin_response_str[idx2:idx1])
                inputs_flag.append(1)

                idx2 = i2.end()

                # exec result
                inputs_str.append(origin_response_str[idx1:idx2])
                inputs_flag.append(0)

            if idx2 != len(origin_response_str):
                inputs_str.append(origin_response_str[idx2:])
                inputs_flag.append(1)

        if len(inputs_flag) == 1:
            continue
        all_inputs_str.append(inputs_str)
        all_inputs_flag.append(inputs_flag)

    raw_data=origin_data[data_index]
    post_data = {
        'inputs': all_inputs_str,
        'flags': all_inputs_flag
    }

    return raw_data,post_data



def get_ms_tool_dataset_test(file_path:str,data_index:int):
    # ms_tool_dataset: for train
    # each data may contain multiple segments, they are organized as different samples
    all_inputs_str = []
    all_labels_str = []

    if os.path.isfile(file_path):
        dataset_json_file=file_path
        with open(dataset_json_file, 'r') as f:
            if dataset_json_file.endswith('.json'):
                origin_data = json.load(f)
            elif dataset_json_file.endswith('.jsonl'):
                origin_data = []
                for line in f:
                    origin_data.append(json.loads(line))
    else:
        raise ValueError("数据集不存在！")

    for i, d in enumerate(origin_data):
        if data_index != i:
            continue
        content = d['conversations']
        if isinstance(content, str):
            content = ast.literal_eval(content)

        # ilegal data
        if len(content) == 0 or content[0]['from'] != 'system':
            continue

        system_str = '<|system|>:' + content[0]['value']

        input_str = system_str

        for i in range(len(content) // 2):
            if len(content[2 * i + 2]['value']) == 0:
                continue

            assert content[2 * i + 1]['from'] == 'user'
            assert content[2 * i + 2]['from'] == 'assistant'
            # user input
            input_str += ('\n\n<|user|>:' + content[2 * i + 1]['value'])

            # assistant response
            origin_response_str = '\n\n<|assistant|>:' + content[2 * i
                                                                 + 2]['value']

            idx2 = 0

            iter1 = re.finditer(r'<\|startofexec\|>', origin_response_str)
            iter2 = re.finditer(r'<\|endofexec\|>', origin_response_str)

            for i1, i2 in zip(iter1, iter2):
                idx1 = i1.start()

                # llm response
                llm_response = origin_response_str[idx2:idx1]
                all_inputs_str.append(input_str)
                all_labels_str.append(llm_response)

                input_str += llm_response

                idx2 = i2.end()

                # exec result
                exec_result = origin_response_str[idx1:idx2]
                input_str += exec_result

            # summarize
            if idx2 != len(origin_response_str):
                final_summarize = origin_response_str[idx2:]
                all_inputs_str.append(input_str)
                all_labels_str.append(final_summarize)

    dataset = {
        'inputs': all_inputs_str,
        'labels': all_labels_str
    }
    input_label_list=[]
    for inp,label in list(zip(all_inputs_str,all_labels_str)):
        input_label_list.append({"input":inp,"label":label})
    return dataset,input_label_list