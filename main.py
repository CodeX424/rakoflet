from flet import *
import pytesseract
from PIL import Image
import io
import openai


openai.api_key = 'your_openai_api_key'


def extract_text_from_image(image_file):
    try:
        img = Image.open(io.BytesIO(image_file))
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"Error extracting text: {e}"


def analyze_with_ai(text):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Analyze the following text:\n{text}",
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error analyzing text with AI: {e}"

def main(page: Page):
    page.add(Text("AI Chat Scanner App", size=30, weight="bold"))
    
   
    file_picker = FilePicker(on_result=lambda e: on_file_selected(e, page))
    page.add(file_picker)
    
    password_input = TextField(label="Enter password to use AI", password=True)
    page.add(password_input)
    
    normal_scan_button = ElevatedButton("الفحص العادي", on_click=lambda e: on_normal_scan(page))
    ai_scan_button = ElevatedButton("استخدام AI", on_click=lambda e: on_ai_scan(password_input, page))
    
    page.add(normal_scan_button, ai_scan_button)
    
    result_text = Text("")
    page.add(result_text)

    page.update()

def on_file_selected(e, page):
    if e.files:
        file = e.files[0]
        with open(file.path, "rb") as f:
            image_file = f.read()
            extracted_text = extract_text_from_image(image_file)
            page.controls[4].value = extracted_text
            page.update()

def on_normal_scan(page):
    page.controls[4].value = "فحص عادي تم بنجاح!"
    page.update()

def on_ai_scan(password_input, page):
    if password_input.value == "09092009":
        extracted_text = page.controls[4].value
        if extracted_text:
            ai_analysis = analyze_with_ai(extracted_text)
            page.controls[4].value = f"تحليل AI:\n{ai_analysis}"
        else:
            page.controls[4].value = "يرجى اختيار صورة لاستخراج النص أولاً."
    else:
        page.controls[4].value = "كلمة المرور غير صحيحة!"
    page.update()

app(main)
