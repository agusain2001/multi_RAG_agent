import google.generativeai as genai

genai.configure(api_key="AIzaSyBq0G6j6foIY69LcVGK6s2Dr_-5ejWdwB4")

def generate_answer(query, context):
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"Answer based on context:\n{context}\n\nQuestion: {query}"
    response = model.generate_content(prompt)
    return response.text