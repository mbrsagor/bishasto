from enum import IntEnum


class GENDER(IntEnum):
    MALE = 0
    FEMALE = 1
    OTHERS = 2

    @classmethod
    def select_gender(cls):
        return [(key.value, key.name) for key in cls]


class ROLE(IntEnum):
    ADMIN = 0
    MANAGER = 1
    SHOPKEEPER = 2
    DELIVERY_MAN = 3
    CUSTOMER = 4

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]


# Add role permission
allow_access_admin = ROLE.Admin.value
allow_access_manager = ROLE.MANAGER.value
allow_shopkeeper = ROLE.SHOPKEEPER.value
allow_customer = ROLE.CUSTOMER.value
allow_delivery_man = ROLE.DELIVERY_MAN.value


class LOCATIONCHOICES(IntEnum):
    COUNTRY = 0
    CITY = 1
    AREA = 2
    THANA = 3
    POSTCODE = 4
    DIVISION = 5

    @classmethod
    def location_type_choices(cls):
        return [(key.value, key.name) for key in cls]


class TYPES(IntEnum):
    KG = 0
    PCS = 1
    BOX = 2

    @classmethod
    def select_types(cls):
        return [(key.value, key.name) for key in cls]


class PROGRESS(IntEnum):
    PENDING = 0
    CANCEL = 1
    FAILED = 2
    PROCESSING = 3
    DELIVERY = 4
    DONE = 5

    @classmethod
    def order_status(cls):
        return [(key.value, key.name) for key in cls]


class PAYMENT(IntEnum):
    CASH_ON_DELIVERY = 0
    BKASH = 1
    NOGOD = 2
    BANK = 3

    @classmethod
    def payment_choices(cls):
        return [(key.value, key.name) for key in cls]
