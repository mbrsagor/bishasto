import firebase_admin
from firebase_admin import credentials, firestore

# Use a service account.
cred = credentials.Certificate("utils/service-account.json")

app = firebase_admin.initialize_app(cred)
db = firestore.client()


def send_message(interest, admin, customer, message, url, button, attachment):
    """
    Name: Send message to firebase from the system.
    Description: Send message to
    :param interest:
    :param admin:
    :param customer:
    :param message:
    :param url:
    :param button:
    :param attachment:
    :return:
    """

    message_ref = db.collection('messages')
    return message_ref.add(
        {
            'interest': interest,
            'admin': admin,
            'customer': customer,
            'message': message,
            'url': url,
            'button': button,
            'attachment': attachment
        }
    )


