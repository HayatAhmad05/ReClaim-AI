import openai
from dotenv import load_dotenv
from io import BytesIO
import os, uuid
from PIL import Image
import base64
import json
from models import ReceiptData, ChildFeeForm
from form_fill import fill_child_fee_pdf
from pdf2image import convert_from_path

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY", "").strip()


reciept_system_prompt = (
    "You are an expert at extracting data from receipts. "
    "Read the provided image of a receipt and return a JSON object that matches the following Pydantic model:\n"
    "from typing import List, Optional\n"
    "class ReceiptItem(BaseModel):\n"
    "    description: str\n"
    "    amount: float\n\n"
    "class ReceiptData(BaseModel):\n"
    "    merchant: str\n"
    "    date: str\n"
    "    total_amount: float\n"
    "    items: Optional[List[ReceiptItem]] = None\n"
    "- Extract only the above given information.\n"
    "- If a value is missing, set it to null, \"\", or an empty list as appropriate.\n"
    "- For the items field, provide a list of objects with description and amount.\n"
    "- Only return a valid JSON object matching the model above.\n"
    "- Do not add any explanation or extra text—only the JSON."
)

fee_bill_system_prompt = (
    "You are an expert at extracting data from fee bills. "
    "Read the provided image of a child fee bill and return a JSON object that matches the following Pydantic model:\n"
    "from typing import List, Optional\n"
    "class FeeItem(BaseModel):\n"
    "    bill_date: Optional[str] = None  # Bill Date Field, leave null if not found\n"
    "    description: str\n"
    "    amount: float\n\n"
    "    bill_month: Optional[str] = None  # Bill Month Field, leave null if not found\n"
    "class FeeBillData(BaseModel):\n"
    "    items: List[FeeItem]\n"
    "    total: float\n"
    "- Extract only the above given information.\n"
    "- If a value is missing, set it to null, \"\", or an empty list as appropriate.\n"
    "- For the items field, provide a list of objects with date, description, and amount.\n"
    "- The total field must be the sum of all amount values in items.\n"
    "- Only return a valid JSON object matching the model above.\n"
    "- Do not add any explanation or extra text—only the JSON."
)




def pil_to_bytes(pil_img, quality=60):
    buf = BytesIO()
    pil_img.save(buf, format='JPEG', quality=quality)
    buf.seek(0)
    return buf


def preprocess_image(pil_img, max_size=512):
    return pil_img.resize((max_size, max_size), Image.LANCZOS)


def extract_info(pil_img):
    processed_image = preprocess_image(pil_img)
    img_bytes = pil_to_bytes(processed_image)
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": reciept_system_prompt

            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Here is a receipt image:"},
                    {"type": "image_url", "image_url": {"url": "data:image/png;base64," + img_base64}}
                ]
            }
        ]
    )

    raw_output = response.choices[0].message.content
    # print(raw_output)
    try:
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("` \n")
            if raw_output.startswith("json"):
                raw_output = raw_output[4:].strip()
        data = json.loads(raw_output)
        print(data)
        validated = ReceiptData(**data)
        json_block = json.dumps(validated.dict(), indent=2, ensure_ascii=False)
        return f"```json\n{json_block}\n```"
    except Exception as e:
        return f"```json\n{json.dumps({'error': str(e), 'raw_output': raw_output}, indent=2)}\n```"


def extract_child_fee_info(img_input, emp_name, emp_code, department):
    print(emp_name, emp_code, department)
    processed_image = preprocess_image(img_input)
    img_bytes = pil_to_bytes(processed_image)
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": fee_bill_system_prompt},
            {"role": "user",
             "content": [
                {"type": "text", "text": "Here is a child fee bill image:"},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + img_base64}}
             ]}
        ]
    )
    raw_output = response.choices[0].message.content
    try:
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("` \n")
            if raw_output.startswith("json"):
                raw_output = raw_output[4:].strip()
        data = json.loads(raw_output)
        print(data)
        # Validate if needed:
        # ChildFeeForm(**data)

        # Extract bill_month from first item if available, else use empty string
        items = data.get("items", [])
        bill_month = ""
        if items and "bill_month" in items[0]:
            bill_month = items[0]["bill_month"]

        os.makedirs("outputs", exist_ok=True)
        output_pdf_path = f"outputs/filled_child_fee_form_{uuid.uuid4().hex}.pdf"


        filled_pdf_path = fill_child_fee_pdf(
            template_pdf_path="CHILD FEE REIMBURSEMENT FORM.pdf",
            output_pdf_path=output_pdf_path,
            emp_name=emp_name,
            emp_code=emp_code,
            department=department,
            bill_month=bill_month,
            items=items,
            total=data.get("total", "")
        )

        return filled_pdf_path # Return path to Gradio for download
    except Exception as e:
        print("ERROR:", e)
        return None  # or f"Error: {str(e)}"
