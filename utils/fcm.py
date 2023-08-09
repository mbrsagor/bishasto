import requests

url = "https://fcm.googleapis.com/fcm/send"
authorization = "authorization_key"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"key={authorization}"
}


def send_notification(send_to, title, message):
    to = send_to
    data = {
        'title': title,
        'message': message
    }
    body = {
        'to': to,
        'data': data
    }
    response = requests.post(url, json=body, headers=headers)
    return response
