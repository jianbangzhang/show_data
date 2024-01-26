import ast
import re
from utils import read_jsonl







def get_ms_tool_dataset(file_path:str,data_index:int) -> tuple:
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


