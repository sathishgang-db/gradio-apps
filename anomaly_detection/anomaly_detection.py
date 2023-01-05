import gradio as gr
from example import list_of_examples
from scoring_func import update

with gr.Blocks() as demo:
    gr.Markdown("## Real Time Anomaly Detection using Databricks ML 🕵️‍♂️!")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Enter values for fields (hint 🦻: use any example for a quick demo):")
            inp = [
                gr.Textbox(label="Machine ID", placeholder="What is the MacID?"),
                gr.Textbox(label="Time ID", placeholder="What is the Time ID?"),
                gr.Textbox(label="Sensor1", placeholder="Value1"),
                gr.Textbox(label="Sensor2", placeholder="Value2"),
                gr.Textbox(label="Sensor3", placeholder="Value3"),
                gr.Textbox(label="Sensor4", placeholder="Value4"),
                gr.Textbox(label="Sensor5", placeholder="Value5"),
                gr.Textbox(label="Sensor6", placeholder="Value6"),
                gr.Textbox(label="Sensor7", placeholder="Value7"),
                gr.Textbox(label="Sensor8", placeholder="Value8"),
                gr.Textbox(label="Sensor9", placeholder="Value9"),
                gr.Textbox(label="Sensor10", placeholder="Value10"),
                gr.Textbox(label="Sensor11", placeholder="Value11"),
                gr.Textbox(label="Sensor12", placeholder="Value12"),
                gr.Textbox(label="Sensor13", placeholder="Value13"),
                gr.Textbox(label="Sensor14", placeholder="Value14"),
                gr.Textbox(label="Sensor15", placeholder="Value15"),
                gr.Textbox(label="Sensor16", placeholder="Value16"),
                gr.Textbox(label="Sensor17", placeholder="Value17"),
                gr.Textbox(label="Sensor18", placeholder="Value18"),
                gr.Textbox(label="Sensor19", placeholder="Value19"),
                gr.Textbox(label="Sensor20", placeholder="Value20"),
                gr.Textbox(label="Sensor21", placeholder="Value21"),
                gr.Textbox(label="Sensor22", placeholder="Value22"),
                gr.Textbox(label="Sensor23", placeholder="Value23"),
                gr.Textbox(label="Sensor24", placeholder="Value24"),
                gr.Textbox(label="Sensor25", placeholder="Value25"),
                gr.Textbox(label="Sensor26", placeholder="Value26"),
                gr.Textbox(label="Sensor27", placeholder="Value27"),
                gr.Textbox(label="Sensor28", placeholder="Value28"),
            ]
        with gr.Column():
            gr.Markdown("### Output populates below! 🏁")
            out = gr.Textbox(label="Model Scoring Result", placeholder="Is this an anomaly?")
            gr.Examples(list_of_examples, inputs=inp, outputs=out, fn=update, label="Click example to pre-fill fields(all are GT anomalies):")
            btn = gr.Button("Run")
    btn.click(fn=update, inputs=inp, outputs=out)

demo.launch()
