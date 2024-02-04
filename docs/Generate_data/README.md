# mm-chatocr 数据生成教程
**以微调证书信息提取相关数据为例**
-
依旧使用的是文心一言构建的数据集。

配置环境：
```python
pip install erniebot
pip install paddlepaddle==2.6.0
pip install paddleocr
```
设计Prompt:
```python
input = f''' 
             OCR的文字识别结果使用```符号包围，包含所识别出来的文字，顺序在原始图片中从左至右、从上至下。我指定的关键信息使用[]符号包围。请注意OCR的文字识别结果可能存在长句子换行被切断、不合理的分词、对应错位等问题，你需要结合上下文语义进行综合判断，以抽取准确的关键信息。在返回结果时使用json格式，包含一个key-value对，key值为我指定的关键信息，value值为所抽取的结果。
             如果认为OCR识别结果中没有关键信息key，则将value赋值为“未找到相关信息”。 
             在级别中，如果出现“初赛”俩字或者“省”字则将value赋值为“省赛”，其余均默认为“国赛”。
             在等级中，如果未出现几等奖，则将value赋值为“获奖”，其余均按照实际奖项赋值。
             请只输出json格式的结果，不要包含其它多余文字！下面正式开始：
                    OCR文字：```{ocr_result}```
                    要抽取的关键信息：[{key}]。
            '''
```


主要代码：

导包
```python
import os 
import glob  
import time 
import json
import erniebot
from  paddleocr  import  PaddleOCR 

```

设置参数
```python
model = 'ernie-3.5'
erniebot.api_type = 'aistudio'
erniebot.access_token = "你的访问令牌"
data_path = '你的证书文件夹路径'
folder_path = f'{data_path}'  
key = '姓名, 比赛名称, 证书编号, 指导老师姓名, 级别,等级, 证书日期, 比赛单位承办单位'  # 要提取的字段
system_prompt = '现在你是一个信息提取专家，你现在的任务是从OCR文字识别的结果中提取我指定的关键信息。'
# image_files = glob.glob(os.path.join(folder_path, '*.jpg')) + glob.glob(os.path.join(folder_path, '*.png')) + glob.glob(os.path.join(folder_path, '*.jpeg'))
```

拿到相关证书存放地址

```python
import os  
  
def get_image_paths(directory):  
    image_paths = []  
    for root, dirs, files in os.walk(directory):  
        for file in files:  
            if file.endswith('.jpg') or file.endswith('.png'):  
                image_paths.append(os.path.join(root, file))  
    return image_paths  
  
# 调用函数，传入你的文件夹路径  
image_files = get_image_paths('/home/aistudio/work/获奖图像')  
print(len(image_files))
# 打印所有图片路径  
for path in image_files:  
    print(path)
```

生成对应结果

```python
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
result_last = []
for file_path in image_files:
    conversation = {'conversation':[]}
    result  =  ocr.ocr(file_path, cls=True) 
    print(f"正在处理{file_path}")
    ocr_result = ""
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
    #         print(line[1][0])
            ocr_result = ocr_result + " " + str(line[1][0])
            
    input = f''' 
             OCR的文字识别结果使用```符号包围，包含所识别出来的文字，顺序在原始图片中从左至右、从上至下。我指定的关键信息使用[]符号包围。请注意OCR的文字识别结果可能存在长句子换行被切断、不合理的分词、对应错位等问题，你需要结合上下文语义进行综合判断，以抽取准确的关键信息。在返回结果时使用json格式，包含一个key-value对，key值为我指定的关键信息，value值为所抽取的结果。
             如果认为OCR识别结果中没有关键信息key，则将value赋值为“未找到相关信息”。 
             在级别中，如果出现“初赛”俩字或者“省”字则将value赋值为“省赛”，其余均默认为“国赛”。
             在等级中，如果未出现几等奖，则将value赋值为“获奖”，其余均按照实际奖项赋值。
             请只输出json格式的结果，不要包含其它多余文字！下面正式开始：
                    OCR文字：```{ocr_result}```
                    要抽取的关键信息：[{key}]。
            '''
    
    messages = [{'role': 'user', 'content': f"{input.strip()}"}]
    while True:
        try :
            first_response = erniebot.ChatCompletion.create(
                model=model,
                messages=messages,
            )
            break
        except:
                    time.sleep(5)
                    continue
    out_put = first_response.result
    print('=========================')
    print(out_put)
    q_a = {'system':system_prompt, 'input':input, 'output':out_put}
    conversation = {'conversation':[q_a,]}
    result_last.append(conversation)

```
保存为json文件
```python

with open(f'/home/aistudio/work/res.json', 'w', encoding='utf-8') as file:  
        json.dump(result_last, file, ensure_ascii=False, indent=4)
    
```