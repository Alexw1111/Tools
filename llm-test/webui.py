#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen3-0.6B 翻译程序 - 基于 llama.cpp 的轻量级翻译工具
"""

import os
import sys
import gradio as gr
from typing import Optional
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# 模型配置 - 只需要修改这里
REPO_ID = "Qwen/Qwen3-0.6B-GGUF"
MODEL_FILE = "Qwen3-0.6B-Q8_0.gguf"
MODEL_PATH = f"models/{MODEL_FILE}"


def download_model(model_path: str) -> bool:
    """使用HuggingFace Hub自动下载模型"""
    try:
        print("正在下载模型...")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # 使用HuggingFace Hub下载模型
        downloaded_path = hf_hub_download(
            repo_id=REPO_ID,
            filename=MODEL_FILE,
            local_dir=os.path.dirname(model_path),
            local_dir_use_symlinks=False
        )
        
        # 重命名为预期的文件名
        if downloaded_path != model_path:
            import shutil
            shutil.move(downloaded_path, model_path)
        
        print("模型下载完成！")
        return True
        
    except Exception as e:
        print(f"下载失败: {e}")
        return False


class QwenTranslator:
    def __init__(self, model_path: str):
        """初始化Qwen翻译器"""
        self.model_path = model_path
        self.llm: Optional[Llama] = None
        
    def load_model(self):
        """加载模型"""
        if not os.path.exists(self.model_path):
            print("模型文件未找到，正在自动下载...")
            if not download_model(self.model_path):
                return False, "模型下载失败"
            
        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=4,
                verbose=False
            )
            return True, "模型加载成功！"
        except Exception as e:
            return False, f"模型加载失败: {e}"
    
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """翻译文本"""
        if not self.llm:
            return "模型未加载，请先加载模型。"
        
        if not text.strip():
            return "请输入要翻译的文本"
        
        # 构建翻译提示词
        prompt = self._build_translate_prompt(text, source_lang, target_lang)
        
        try:
            response = self.llm(
                prompt,
                max_tokens=512,
                temperature=0.3,
                top_p=0.9,
                stop=["<|im_end|>"],
                echo=False
            )
            
            return response['choices'][0]['text'].strip()
            
        except Exception as e:
            return f"翻译时出错: {e}"
    
    def _build_translate_prompt(self, text: str, source_lang: str, target_lang: str) -> str:
        """构建翻译提示词"""
        system_prompt = (f"你是一个专业的翻译助手。"
                        f"请将以下{source_lang}文本翻译成{target_lang}。/no_think "
                        f"只返回翻译结果，不要添加其他说明。")
        
        prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        prompt += f"<|im_start|>user\n{text}<|im_end|>\n"
        prompt += "<|im_start|>assistant\n"
        
        return prompt


def create_interface(model_path: str):
    """创建简洁的翻译界面"""
    
    # 初始化翻译器
    translator = QwenTranslator(model_path)
    
    # 尝试加载模型
    model_loaded, load_message = translator.load_model()
    
    with gr.Blocks(title="翻译器") as app:
        
        gr.Markdown("## 翻译器")
        
        # 翻译方向选择
        direction = gr.Radio(
            choices=["中→英", "英→中"],
            value="中→英",
            label="翻译方向"
        )
        
        # 翻译区域
        input_text = gr.Textbox(
            placeholder="输入要翻译的文本...",
            label="原文",
            lines=6
        )
        
        translate_btn = gr.Button("翻译", variant="primary")
        
        output_text = gr.Textbox(
            label="译文",
            lines=6,
            interactive=False
        )
        
        # 状态显示
        if not model_loaded:
            gr.Markdown(f"⚠️ {load_message}")
        
        def translate(text: str, dir_choice: str) -> str:
            if not text.strip():
                return ""
            if not model_loaded:
                return "模型加载失败"
            
            if dir_choice == "中→英":
                return translator.translate_text(text, "中文", "英文")
            else:
                return translator.translate_text(text, "英文", "中文")
        
        # 绑定事件
        translate_btn.click(
            translate,
            inputs=[input_text, direction],
            outputs=output_text
        )
        
        input_text.submit(
            translate,
            inputs=[input_text, direction],
            outputs=output_text
        )
    
    return app


def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
    else:
        model_path = MODEL_PATH
    
    print(f"使用模型路径: {model_path}")
    
    # 创建界面
    app = create_interface(model_path)
    
    # 启动服务
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True
    )


if __name__ == "__main__":
    main() 