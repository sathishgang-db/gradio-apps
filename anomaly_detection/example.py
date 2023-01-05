# Local example csv has example data - gets formatted here for the app
import pandas as pd

df = pd.read_csv("example.csv")
examples = df.values.tolist()
list_of_examples = []
for example in examples:
    example = [round(x, 2) for x in example if isinstance(x, float)]
    list_of_examples.append(example)
