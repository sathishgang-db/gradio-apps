#%%
import altair
from databricks import sql
import gradio as gr
from math import sqrt
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd
import toml
import warnings

warnings.filterwarnings("ignore")
from types import SimpleNamespace

config = toml.load("settings.toml")
config = SimpleNamespace(**config.get("adb"))

def _get_connection(config: SimpleNamespace):
    connection = sql.connect(
    server_hostname=config.hostname,
    http_path=config.http_path,
    access_token=config.token,
)
    return connection

connection = _get_connection(config)

query = """select distinct store as Store_ID, dept as Dept_ID 
        from hive_metastore.sgfs.walmart_min_forecasts 
        where store = 1 order by 1,2;"""

data = pd.read_sql(query, connection)

stores = data["Store_ID"].unique().tolist()
departments = data["Dept_ID"].unique().tolist()
connection.close()

def plot_history(store, department):
    connection = _get_connection(config)
    query1 = f"""
        with actuals(date_week,actual_sales,store,dept) as
    (
    select date(`Date`) as date_week , sum(Weekly_Sales) as actual_sales, Store as store, Dept as dept 
    from hive_metastore.sgfs.walmart_cleaned
    where Store = {store} and Dept = {department}
    group by date_week,store, dept
    order by 1
    ),
    forecasts(date_week, forecasts,store,dept) as
    (
    select date_weekly as date_week,forecasts, store, dept from hive_metastore.sgfs.walmart_min_forecasts
    where store = {store} and dept = {department}
    )
    select b.date_week, 
    a.store, 
    a.dept, 
    case when a.forecasts is null then b.actual_sales else a.forecasts end as Sales,
    case when a.forecasts is not null then 'forecasts' else 'actuals' end as Type
    from forecasts as a
    right outer join actuals as b on a.date_week = b.date_week
    order by date_week asc;
    """
    data = pd.read_sql(query1, connection)
    connection.close()
    fig = px.line(
        data,
        x="date_week",
        y="Sales",
        color="Type",
        title=f"Store {store} Department {department} Weekly Sales",
    )
    return fig


inputs = [
    gr.Dropdown(stores, label="Store ID"),
    gr.Dropdown(departments, label="Department ID"),
]
outputs = gr.Plot()

demo = gr.Interface(
    fn=plot_history,
    inputs=inputs,
    outputs=outputs,
    examples=[
        [1, 1],
        [1, 2],
    ],
    cache_examples=True,
)

if __name__ == "__main__":
    demo.launch()
