from pdfrw import PdfReader, PdfWriter
from datetime import datetime

def fill_child_fee_pdf(
    template_pdf_path,
    output_pdf_path,
    emp_name,
    emp_code,
    department,
    bill_month,
    items,   # List of dicts: [{'bill_date': ..., 'description': ..., 'amount': ...}]
    total
):
    data_dict = {
        'emp_name': emp_name,
        'emp_code': emp_code,
        'department': department,
        'bill_month': bill_month,
        'total': str(total),
        'current_date': datetime.now().strftime("%d-%b-%Y"),  # e.g. "25-May-2025"

    }

    # Map each row of items to field names
    for idx, item in enumerate(items, start=1):
        data_dict[f'date_{idx}'] = item.get('bill_date', '')
        data_dict[f'description_{idx}'] = item.get('description', '')
        data_dict[f'amount_{idx}'] = str(item.get('amount', ''))

    # Fill the PDF
    template_pdf = PdfReader(template_pdf_path)
    for page in template_pdf.pages:
        if not hasattr(page, 'Annots') or not page.Annots:
            continue
        for annotation in page.Annots:
            if annotation.T:
                key = annotation.T[1:-1]  # Remove parentheses
                if key in data_dict:
                    annotation.V = str(data_dict[key])
                    annotation.AP = None  # Remove old appearance so new value appears
    PdfWriter().write(output_pdf_path, template_pdf)
    return output_pdf_path


def fill_medical_pdf(
    template_pdf_path,
    output_pdf_path,
    company,
    extension_no,
    employee_name,
    employee_code,
    department,
    date,
    total,
    designation,
    billing_month,
    claims  # List of dicts: [{'name': ..., 'relationship': ..., 'category': ..., 'detail': ..., 'amount': ...}]
):
    data_dict = {
        'company': company,
        'extension_no': extension_no,
        'employee_name': employee_name,
        'employee_code': employee_code,
        'department': department,
        'designation': designation,
        'date': date,
        'billing_month': billing_month,
        'total': str(total),
        'current_date': datetime.now().strftime("%d-%b-%Y"),
    }

    # Map each row of claims to field names
    for idx, claim in enumerate(claims, start=1):
        data_dict[f'name_{idx}'] = claim.get('name', '')
        data_dict[f'relationship_{idx}'] = claim.get('relationship', '')
        data_dict[f'category_{idx}'] = claim.get('category', '')
        data_dict[f'detail_{idx}'] = claim.get('detail', '')
        data_dict[f'amount_{idx}'] = str(claim.get('amount', ''))

    # Fill the PDF
    template_pdf = PdfReader(template_pdf_path)
    for page in template_pdf.pages:
        if not hasattr(page, 'Annots') or not page.Annots:
            continue
        for annotation in page.Annots:
            if annotation.T:
                key = annotation.T[1:-1]  # Remove parentheses
                if key in data_dict:
                    annotation.V = str(data_dict[key])
                    annotation.AP = None  # Remove old appearance so new value appears
    PdfWriter().write(output_pdf_path, template_pdf)
    return output_pdf_path

