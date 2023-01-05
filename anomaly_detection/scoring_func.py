from types import SimpleNamespace
import toml
import requests
import json

config = toml.load("../settings.toml")
config = SimpleNamespace(**config.get("adb"))


def update(
    inp1,
    inp2,
    inp3,
    inp4,
    inp5,
    inp6,
    inp7,
    inp8,
    inp9,
    inp10,
    inp11,
    inp12,
    inp13,
    inp14,
    inp15,
    inp16,
    inp17,
    inp18,
    inp19,
    inp20,
    inp21,
    inp22,
    inp23,
    inp24,
    inp25,
    inp26,
    inp27,
    inp28,
    inp29,
    inp30,
):
    data = [list(locals().values())]
    headers = {
        "Authorization": f"Bearer {config.token}",
        "Content-Type": "application/json",
    }
    payload = json.dumps({"inputs": data})
    url = f"https://{config.hostname}/model-endpoint/sg_anomaly_detection/Staging/invocations"
    response = requests.request(method="POST", headers=headers, url=url, data=payload)
    if response.status_code != 200:
        raise Exception(
            f"Request failed with status {response.status_code}, {response.text}"
        )
    if response.json()["predictions"][0] == 1:
        return "🚨 Anomaly Detected❗️"
    else:
        return "OK 👍"
