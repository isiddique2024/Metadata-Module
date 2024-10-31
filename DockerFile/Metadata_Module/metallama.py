import os
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from dotenv import load_dotenv
import torch
from torch.cuda.amp import autocast

app = Flask(__name__)
load_dotenv()

huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
model_id = "meta-llama/Llama-2-13b-chat-hf"

assert torch.cuda.is_available(), "CUDA is not available. Please check your GPU setup."
device = torch.device("cuda")
print(f"Using device: {device}")

# Optimized quantization configuration
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

tokenizer = AutoTokenizer.from_pretrained(
    model_id, token=huggingface_token, use_fast=True
)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    token=huggingface_token,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
)

print(f"Model loaded and moved to {device}")

# Enable cuda graph for faster inference
model = torch.compile(model)


def generate_prompt(instruction):
    return f"""[INST] <<SYS>>
You are a highly intelligent AI assistant. Provide accurate, concise, and helpful responses.
<</SYS>>

{instruction} [/INST]"""


@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.json
    user_prompt = data.get("prompt", "")

    full_prompt = generate_prompt(user_prompt)
    inputs = tokenizer(full_prompt, return_tensors="pt").to(device)

    try:
        with autocast(dtype=torch.bfloat16):
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=200,
                    do_sample=False,  # Use greedy decoding for speed and consistency
                    num_beams=2,  # Simple beam search for better quality
                    no_repeat_ngram_size=3,
                    num_return_sequences=1,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                )

        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        result = result.replace(full_prompt, "").strip()

        return jsonify({"response": result})
    except Exception as e:
        print(f"Error during generation: {str(e)}")
        return jsonify({"error": "An error occurred during text generation"}), 500


if __name__ == "__main__":
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        model.config.pad_token_id = model.config.eos_token_id

    # TF32 for speed boost
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    print(f"CUDA memory allocated: {torch.cuda.memory_allocated(0) / 1e9:.2f} GB")
    print(f"CUDA memory reserved: {torch.cuda.memory_reserved(0) / 1e9:.2f} GB")

    app.run(debug=False, host="0.0.0.0", port=5000, threaded=False)
