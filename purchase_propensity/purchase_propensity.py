import gradio as gr

import pandas as pd
from types import SimpleNamespace
import toml
import requests
import json

config = toml.load("../settings.toml")
config = SimpleNamespace(**config.get("adb"))

df = pd.read_csv("propensity_ml_example.csv")
examples = df.tail(10).values.tolist()
list_of_examples = []
for example in examples:
    example = [int(x) for x in example if x not in ["hours_since_last_visit","days_since_last_email_open"]]
    list_of_examples.append(example)

def score_text(value):
    if value == 0:
        return "Not Likely to Convert! 🙁"
    else:
        return "Likely to Convert! 🙂"


def score_model(basket_icon_click, basket_add_list, basket_add_detail, sort_by,
       image_picker, account_page_click, promo_banner_click,
       detail_wishlist_add, list_size_dropdown, closed_minibasket_click,
       checked_delivery_detail, checked_returns_detail, sign_in,
       saw_checkout, saw_sizecharts, saw_delivery, saw_account_upgrade,
       saw_homepage, device_mobile, device_computer, device_tablet,
       returning_user, loc_uk, hours_since_last_visit,
       days_since_last_email_open):
    payload = locals()
    headers = {
        "Authorization": f"Bearer {config.token}",
        "Content-Type": "application/json",
    }
    payload = json.dumps({"dataframe_records": [payload]})
    url = f"https://{config.hostname}/model-endpoint/sg_propensity_ml/Staging/invocations"
    response = requests.request(method="POST", headers=headers, url=url, data=payload)
    value  = response.json()['predictions'][0]
    return score_text(value)

with gr.Blocks(title='PropensityML',
css="footer {visibility: hidden}") as demo:
    gr.Markdown("## Customer Propensity to Convert 🛍!")
    gr.Markdown("""* This simple demo shows how AutoML + Databricks ML Serverless Endpoints can be used to create a model that detects customer propensity to convert
    * To try the demo, simple fill in the details of a customer event record OR select an example and click "Score".
    """)
    with gr.Row():
        with gr.Accordion(label = "Click to Modify Customer Event Record Details", open = False):
            inp = [
            gr.Textbox(label="Was the basket clicked?"),
            gr.Textbox(label="Was item added to the basket?"),
            gr.Textbox(label="Was basked info viewed?"),
            gr.Textbox(label="Were search results sorted?"),
            gr.Textbox(label="Product Hero viewed?"),
            gr.Textbox(label="Was account page clicked?"),
            gr.Textbox(label="Was promo banner clicked?"),
            gr.Textbox(label="Was product added to wishlist?"),
            gr.Textbox(label="Was basket size dropdown clicked?"),
            gr.Textbox(label="Was basket clicked?"),
            gr.Textbox(label="Delivery detail checked?"),
            gr.Textbox(label="Returns detail checked?"),
            gr.Textbox(label="Signed In?"),
            gr.Textbox(label="Saw Checkout?"),
            gr.Textbox(label="Saw size charts?"),
            gr.Textbox(label="Saw reviews?"),
            gr.Textbox(label="Saw account upgrade?"),
            gr.Textbox(label="Saw homepage?"),
            gr.Textbox(label="Mobile device?"),
            gr.Textbox(label="Desktop device?"),
            gr.Textbox(label="Tablet device?"),
            gr.Textbox(label="Returning customer?"),
            gr.Textbox(label="Location Enabled?"),
            gr.Textbox(label="Hours Since Last Visit?"),
            gr.Textbox(label="Days Since Last Email Open?"),
            ]

        with gr.Column():
            gr.Markdown("### Output populates below! 🏁")
            out = gr.Textbox(
                label="Customer Propensity to Convert",
                placeholder="Customer",
            )
            gr.Examples(
                list_of_examples,
                inputs=inp,
                outputs=out,
                fn=score_model,
                label="Click example to pre-fill fields(Customer 360 Events):",
            )
            btn = gr.Button("Score")

        btn.click(score_model, inputs=inp,  outputs=out)

demo.launch()

# html for success logo
