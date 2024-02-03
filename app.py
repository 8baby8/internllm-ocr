import gradio as gr
from  paddleocr  import  PaddleOCR, draw_ocr
from PIL import Image

from lmdeploy import turbomind as tm
from openxlab.model import download
from lmdeploy import pipeline, TurbomindEngineConfig, GenerationConfig

download('Farewell1/internlm2-ocrchat-7b',output='model/')

backend_config = TurbomindEngineConfig(cache_max_entry_count=0.1)
gen_config = GenerationConfig(top_p=0.8,
                              top_k=40,
                              temperature=0.8,
                              max_new_tokens=1024)

class ChatOcr():
    def __init__(self, model_path='model/') -> None:
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        self.tm_model = tm.TurboMind.from_pretrained(model_path, model_name='internlm2-chat-7b',engine_config=backend_config)
    
    def geneate_res(self, query):
        self.generator = self.tm_model.create_instance()
        prompt = self.tm_model.model.get_prompt(query)
        input_ids = self.tm_model.tokenizer.encode(prompt)

        # inference
        for outputs in self.generator.stream_infer(
                session_id=0,
                input_ids=[input_ids],
                gen_config=gen_config):
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
        im_show = draw_ocr(image, boxes, txts, scores, font_path='/root/code/chatocr/simfang.ttf')
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
    gr.Markdown("# <center>\N{fire}“mm-chatocr”——基于InternLm2和Paddleocr的信息提取</center>")
    gr.Markdown("<center>\N{fire}时间有限，目前仅支持证书信息的提取,后续会不断迭代，更新应用场景！</center>")
    gr.Markdown()
    with gr.Column():
        with gr.Row():
            image_input = gr.Image(type='filepath')
            # detected_image_output = gr.Image(label="OCR识别结果", type='filepath')  # 新增图像输出组件

        analysis_result = gr.Textbox(label="关键信息提取结果")
        analysis_button = gr.Button("分析图片")

    # analysis_button.click(process_ocr, inputs=image_input, outputs=[detected_image_output, analysis_result])
    analysis_button.click(process_ocr, inputs=image_input, outputs=analysis_result)


demo.launch()