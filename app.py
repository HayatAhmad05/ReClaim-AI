import gradio as gr
from pipeline import extract_info_batch, extract_child_fee_info,extract_medical_info
from PIL import Image





with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Receipts Upload"):
            with gr.Row():
                with gr.Column(scale=2):
                    batch_img_input = gr.File(
                        file_types=["image"],
                        label="Batch Image Upload",
                        elem_id="batch-upload-img",
                        show_label=True,
                        file_count="multiple"
                    )

                with gr.Column(scale=2):
                    batch_output_box = gr.Markdown(
                        value="Upload Images to extract information",
                        label="Batch Extracted Info",
                        elem_id="batch-output-box",
                        show_label=True
                    )
                    batch_img_input.change(
                        fn=extract_info_batch,
                        inputs=batch_img_input,
                        outputs=batch_output_box
                    )
        


        with gr.Tab("Child Fee Reimbursement Form"):
            with gr.Row():
                with gr.Column(scale=2):
                    img_input = gr.Image(
                        type="pil",
                        label="Image Upload",
                        elem_id="upload-img",
                        show_label=False,
                        height=512,
                        width=512
                    )

                with gr.Column(scale=2):
                    # Dropdown for form names
                    gr.Markdown("## Child Fee Reimbursement")
                    
                    # 2x2 grid for info fields
                    with gr.Row():
                        emp_name = gr.Textbox(label="Employee Name")
                
                        emp_code = gr.Textbox(label="Employee Code")
                    with gr.Row():
                        department = gr.Textbox(label="Department")
                    upload_btn = gr.Button("Upload and Process")
                    preview_output = gr.File(label="Download Filled Form")


                    upload_btn.click(
                        fn=extract_child_fee_info,
                        inputs=[img_input, emp_name, emp_code, department],
                        outputs=preview_output
                    )

       
        with gr.Tab("Medical Reimbursement Form"):
            with gr.Row():
                with gr.Column(scale=2):
                    medical_img_input = gr.Image(
                        type="pil",
                        label="Image Upload",
                        elem_id="upload-img",
                        show_label=False,
                        height=512,
                        width=512
                    )
                with gr.Column(scale=2):
                    with gr.Row():
                        med_company_name = gr.Dropdown(choices=["NetSol Technologies Ltd.","NetSol Innovation Private Ltd."], interactive=True, multiselect=False)
                        med_emp_name = gr.Textbox(label="Employee Name")
                        med_department = gr.Textbox(label="Department")
                    with gr.Row():
                        med_designation = gr.Textbox(label="Designation")
                        med_ext_code = gr.Textbox(label="Extention No.")
                        med_emp_code = gr.Textbox(label="Employee Code")
                    medical_upload_btn = gr.Button("Upload and Process")
                    preview_medical_output = gr.File(label="Download Filled Form")

                    
                    medical_upload_btn.click(
                        fn=extract_medical_info,
                        inputs=[medical_img_input,med_emp_name,med_emp_code,med_department,med_designation,med_company_name,med_ext_code],
                        outputs=preview_medical_output
                    )




    # CSS:
    gr.HTML("""
        <style>
        #output-box .prose, #output-box .prose pre, #output-box .prose code {
            font-size: 30px !important;
        }
        </style>
    """)

demo.launch()
