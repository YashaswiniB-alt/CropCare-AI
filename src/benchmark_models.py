import torch
import time
from torchvision import models
import json

torch.set_num_threads(2)

MODEL_PATH = "models/multicrop_mobilenetv3.pth"
OPTIMIZED_PATH = "models/multicrop_mobilenetv3_torchscript.pt"

with open("models/multicrop_labels.json", "r") as f:
    labels = json.load(f)

model = models.mobilenet_v3_small(weights=None)
model.classifier[3] = torch.nn.Linear(
    model.classifier[3].in_features,
    len(labels)
)

checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

optimized_model = torch.jit.load(OPTIMIZED_PATH, map_location="cpu")
optimized_model.eval()

x = torch.randn(1, 3, 224, 224)

def benchmark(model, runs=50):
    with torch.inference_mode():
        for _ in range(10):
            model(x)

        start = time.perf_counter()

        for _ in range(runs):
            model(x)

        elapsed = time.perf_counter() - start

    return (elapsed / runs) * 1000

with torch.inference_mode():
    original_output = model(x)
    optimized_output = optimized_model(x)

original_prediction = original_output.argmax(dim=1).item()
optimized_prediction = optimized_output.argmax(dim=1).item()

original_time = benchmark(model)
optimized_time = benchmark(optimized_model)

print("\n===== MODEL BENCHMARK =====")
print("Original prediction:", labels[original_prediction])
print("Optimized prediction:", labels[optimized_prediction])
print("Predictions match:", original_prediction == optimized_prediction)
print(f"Original inference: {original_time:.2f} ms")
print(f"TorchScript inference: {optimized_time:.2f} ms")

if original_time > 0:
    speedup = original_time / optimized_time
    print(f"Speedup: {speedup:.2f}x")
    print(f"Latency reduction: {(1-optimized_time/original_time)*100:.2f}%")