import requests

path_to_local_webhook = "/webhook"
current_url = (
    "https://3013-195-19-121-46.ngrok-free.app" + path_to_local_webhook
)
current_token = "5557386036:AAG6H5f_6JE5hVLYx5MH2BZLwbZ1w2lJmRw"
# current_token = "5557386036:AAG6H5f_6JE5hVLYx5MH2BZLwbZ1w2lJmRw"

template = "https://api.telegram.org/bot{token}/{method}"

set_webhook = 0


if set_webhook:
    print(
        requests.get(
            template.format(token=current_token, method="setWebhook"),
            params={"url": current_url},
        ).json()
    )
else:
    print(
        requests.get(
            template.format(token=current_token, method="deleteWebhook"),
            params={"url": current_url},
        ).json()
    )
