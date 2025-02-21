import re
import ollama


def summarize_text_with_ai(input_file: str, output_file: str):
    """Reads a scraped text file, sends it to AI for summarization, and saves the result."""
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            text_content = file.read()

        response = ollama.chat(
            model="deepseek-r1",
            messages=[
                {"role": "system", "content": "Summarize the key points from the comments."},
                {"role": "user", "content": text_content}
            ]
        )

        ai_summary = response["message"]["content"]

        # Remove "<think>...</think>" sections
        ai_summary_cleaned = re.sub(r"<think>.*?</think>", "", ai_summary, flags=re.DOTALL).strip()

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(ai_summary_cleaned)

        print(f"✅ AI summary saved successfully: {output_file}")

    except Exception as e:
        print(f"❌ Error: Failed to summarize text. {e}")
