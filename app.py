import gradio as gr
from pipeline import extract_info, extract_child_fee_info
from pdf2image import convert_from_path



with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Single Upload"):
            with gr.Row():
                with gr.Column(scale=2):
                    img_input = gr.Image(type="pil",label="Image Upload",elem_id="upload-img",show_label=False,height=512,width=512)

                with gr.Column(scale=2):
                    output_box = gr.Markdown(
                        value="""```json
                                    {
                                    "merchant": "",
                                    "date": "",
                                    "total_amount": null,
                                    }
                                    ```""",

                        label="Extracted Info", elem_id="output-box", show_label=False
                    )
                    img_input.upload(fn=extract_info, inputs=img_input, outputs=output_box)
        



        with gr.Tab("Reimbursement Form"):
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
                    form_dropdown = gr.Dropdown(
                        choices=["Child Fee Reimbursement", "Medical Reimbursement", "Other Form"],
                        label="Select Form",
                        value="Child Fee Reimbursement",
                        multiselect=False,
                        interactive=True,
                    )
                    
                    # 2x2 grid for info fields
                    with gr.Row():
                        emp_name = gr.Textbox(label="Employee Name")
                        emp_code = gr.Textbox(label="Employee Code")
                    with gr.Row():
                        department = gr.Textbox(label="Department")
                    upload_btn = gr.Button("Upload and Process")
                    preview_output = gr.Markdown(label="Filled Form")


                    upload_btn.click(
                        fn=extract_child_fee_info,
                        inputs=[img_input, emp_name, emp_code, department],
                        outputs=preview_output
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
