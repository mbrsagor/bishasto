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
    DELIVERYBOY = 3
    CUSTOMER = 4

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]
