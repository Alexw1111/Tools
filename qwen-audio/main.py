import os
import csv
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch

torch.manual_seed(1234)

# 请注意：分词器默认行为已更改为默认关闭特殊token攻击防护。
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-Audio-Chat", trust_remote_code=True)

# 打开bf16精度，A100、H100、RTX3060、RTX3070等显卡建议启用以节省显存
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-Audio-Chat", device_map="auto", trust_remote_code=True, bf16=True).eval()
# 打开fp16精度，V100、P100、T4等显卡建议启用以节省显存
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-Audio-Chat", device_map="auto", trust_remote_code=True, fp16=True).eval()
# 使用CPU进行推理，需要约32GB内存
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-Audio-Chat", device_map="cpu", trust_remote_code=True).eval()
# 默认gpu进行推理，需要约24GB显存
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-Audio-Chat", device_map="cuda", trust_remote_code=True).eval()

def transcribe_audio(audio_path):
    query = tokenizer.from_list_format([
        {'audio': audio_path},  # 音频文件路径或URL
        {'text': 'Please transcribe the audio.'},  # 请求模型转录音频的提示
    ])

    response, _ = model.chat(tokenizer, query=query, history=None)
    return response

# 提供包含音频文件的文件夹路径
audio_folder = 'path/to/your/audio/folder'

# 获取文件夹中所有的音频文件
audio_files = [file for file in os.listdir(audio_folder) if file.endswith('.flac')]

# 指定输出的CSV文件路径
output_file = 'transcriptions.csv'

# 打开CSV文件并写入转录结果
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Audio Path', 'Transcription'])  # 写入表头

    for audio_file in audio_files:
        audio_path = os.path.join(audio_folder, audio_file)
        transcription = transcribe_audio(audio_path)
        writer.writerow([audio_path, transcription])  # 写入音频路径和转录结果

print(f"Transcriptions saved to {output_file}")