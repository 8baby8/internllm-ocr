import gradio as gr
from  paddleocr  import  PaddleOCR, draw_ocr
from PIL import Image

from lmdeploy import turbomind as tm
from openxlab.model import download
from lmdeploy import pipeline, TurbomindEngineConfig, GenerationConfig

download('Farewell1/internlm2-ocrchat-7b',output='model/')

backend_config = TurbomindEngineConfig(cache_max_entry_count=0.1)
# gen_config = GenerationConfig(top_p=0.8,
#                               top_k=40,
#                               temperature=0.8,
#                               max_new_tokens=1024)

class ChatOcr():
    def __init__(self, model_path='model/') -> None:
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        self.tm_model = tm.TurboMind.from_pretrained(model_path, model_name='internlm2-chat-7b',engine_config=backend_config)
    
    def geneate_res(self, query, key='姓名, 比赛名称, 证书编号, 指导老师姓名, 级别,等级, 证书日期, 比赛单位承办单位'):
        tmp_query = f''' 
             OCR的文字识别结果使用```符号包围，包含所识别出来的文字，顺序在原始图片中从左至右、从上至下。我指定的关键信息使用[]符号包围。请注意OCR的文字识别结果可能存在长句子换行被切断、不合理的分词、对应错位等问题，你需要结合上下文语义进行综合判断，以抽取准确的关键信息。在返回结果时使用json格式，包含一个key-value对，key值为我指定的关键信息，value值为所抽取的结果。
             如果认为OCR识别结果中没有关键信息key，则将value赋值为“未找到相关信息”。 
             在级别中，如果出现“初赛”俩字或者“省”字则将value赋值为“省赛”，其余均默认为“国赛”。
             在等级中，如果未出现几等奖，则将value赋值为“获奖”，其余均按照实际奖项赋值。
             请只输出json格式的结果，不要包含其它多余文字！下面正式开始：
                    OCR文字：```{query}```
                    要抽取的关键信息：[{key}]。
            '''
        self.generator = self.tm_model.create_instance()
        prompt = self.tm_model.model.get_prompt(tmp_query)
        input_ids = self.tm_model.tokenizer.encode(prompt)

        # inference
        for outputs in self.generator.stream_infer(
                session_id=0,
                input_ids=[input_ids]):
                # gen_config=gen_config):
            print(outputs[0])
            # print(len(outputs[0]))
            _type_, res, tokens = outputs

        response = self.tm_model.tokenizer.decode(res)
        return response

    def process_file(self, file_path):
        print('==============================')
        print(f"正在处理{file_path}")
        self.result  =  self.ocr.ocr(file_path, cls=True) 
        self.ocr_result = ""
        for idx in range(len(self.result)):
            res = self.result[idx]
            for line in res:
        #         print(line[1][0])
                self.ocr_result = self.ocr_result + " " + str(line[1][0])

        result = self.result[0]
        print(file_path)
        image = Image.open(file_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='./simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save('result.jpg')
        chatocr_res = self.geneate_res(self.ocr_result)
        return chatocr_res

    
# chatocr = ChatOcr(model_path='/root/code/chatocr/last_weight')
chatocr = ChatOcr()

process_ocr = chatocr.process_file
# print(process_ocr)
### Gradio UI ###
with gr.Blocks() as demo:
    gr.Markdown("# <center>\N{fire}“mm-chatocr”——基于InternLm2和OCR的信息提取</center>")
    gr.Markdown("<center>\N{fire}时间有限，目前仅支持证书信息的提取,后续会不断迭代，更新应用场景！</center>")
    gr.Markdown()
    with gr.Column():
        with gr.Row():
            image_input = gr.Image(type='filepath')
            detected_image_output = gr.Image(label="OCR识别结果", type='filepath')  # 新增图像输出组件

        analysis_result = gr.Textbox(label="关键信息提取结果")
        analysis_button = gr.Button("分析图片")

    analysis_button.click(process_ocr, inputs=image_input, outputs=[detected_image_output, analysis_result])
    # analysis_button.click(process_ocr, inputs=image_input, outputs=analysis_result)


demo.launch()