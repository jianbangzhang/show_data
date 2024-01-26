


def describe_data():
    data_string="数据集主要包括了四种：AI模型API，通用API，API无关通用sft数据，API检索增强数据"
    data_detail="""system: 表示给模型前置的人设输入，其中有告诉模型如何调用插件以及生成请求
                user: 表示用户的输入prompt，分为两种，通用生成的prompt和调用插件需求的prompt
                assistant: 为模型的回复。其中会包括插件调用代码和执行代码，调用代码是要LLM生成的，而执行代码是调用服务来生成结果的。如下面例子，调用部分代码会通过<|startofthink|>和<|endofthink|>包起来，>然后执行部分代码是api执行完结果后，把执行结果通过<|startofexec|>和<|endofexec|>包起来再输入给模型生成后面的回复"""
    data_note="""Each data instance consists of three roles: system, user, and assistant. The LLM should only focus on the assistant part.
                The assistant part is typically composed of three sections. The LLM should only consider the content of the agent call and the final summary.
                The other unnecessary parts are masked using IGNORE_INDEX to exclude them from loss calculation."""

    return data_string,data_detail,data_note