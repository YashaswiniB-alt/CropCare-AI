import ollama

MODEL_NAME = "qwen2.5:3b"


def ask_farmer_ai(question, scan_context=None):
    try:
        system_prompt = (
    "You are CropCare AI, a helpful agricultural assistant. "
    "Answer farmers in simple English. Explain crop diseases, "
    "plant symptoms, prevention, irrigation, and crop care. "
    "Give practical, safe advice. Do not invent certainty. "
    "If a diagnosis is uncertain, recommend consulting a local "
    "agricultural expert. Avoid recommending dangerous chemical doses. "
    "If scan results are provided, use them to personalize your answer. "
    "Treat the model's disease prediction as a possibility, not a confirmed diagnosis. "
    "Do not claim that the visible damage percentage is laboratory-verified."
) 

        if scan_context:
            user_message = (
                "LATEST PLANT SCAN RESULTS:\n"
                f"{scan_context}\n\n"
                "FARMER'S QUESTION:\n"
                f"{question}"
            )
        else:
            user_message = question

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"AI Assistant error: {e}"