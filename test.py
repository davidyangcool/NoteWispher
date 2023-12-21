
import whisper
model_path = "./whisper-models/medium.pt"

# 使用Whisper的API加载模型
model = whisper.load_model(model_path)
result = model.transcribe("/Users/david/Desktop/Vocabulary/1.mp3",  fp16="False")
print(result)
