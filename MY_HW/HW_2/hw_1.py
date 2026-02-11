#######Task_1###########
# from pydantic import BaseModel, Field, model_validator, EmailStr
#
#
# class Address(BaseModel):
#     city: str = Field(min_length=2)
#     street: str = Field(min_length=3)
#     house_number: int = Field(gt=0)
#
#
# class User(BaseModel):
#     name: str = Field(min_length=2, pattern="[A-Za-zА-Яа-яЁё]+")
#     age: int = Field(ge=0, le=120)
#     email: str = EmailStr
#     is_employed: bool = Field()
#     address: Address
#
#
#     @model_validator(mode="after")
#     def check_age_for_employed(self) -> "User":
#         if self.is_employed and not (18 <= self.age <= 65):
#             raise ValueError("Если пользователь занят (is_employed=true), возраст должен быть от 18 до 65 лет")
#         return self
#
#
# address = Address(
#     city="Berlin",
#     street="Main Street",
#     house_number=3
# )
#
# user = User(
#     name="John",
#     age=32,
#     email="john.doe@example.com",
#     is_employed=True,
#     address=address
# )
#
# print(user)

#######Task_2###########
from pydantic import BaseModel, ValidationError, Field, EmailStr, model_validator


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    name: str = Field(min_length=2, pattern="[A-Za-zА-Яа-яЁё]+")
    age: int = Field(ge=0, le=120)
    email: str = EmailStr
    is_employed: bool = Field()
    address: Address

    @model_validator(mode="after")

    def check_age_for_employed(self) -> "User":
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError("Если пользователь занят (is_employed=true), возраст должен быть от 18 до 65 лет")
        return self


json_input = """{

    "name": "John Doe",

    "age": 65,

    "email": "john.doe@example.com",

    "is_employed": true,

    "address": {

        "city": "New York",

        "street": "5th Avenue",

        "house_number": 123

    }

}"""

json_input2 = """{

    "name": "Tomas",

    "age": 25,

    "email": "tomas.doe@gmail.com",

    "is_employed": true,

    "address": {

        "city": "Kassel",

        "street": "Ständeplatz",

        "house_number": 25

    }

}"""


def get_json(json_str: str) -> str:
    try:
        user = User.model_validate_json(json_str)
        convert_in_json = user.model_dump_json()
        return convert_in_json
    except ValidationError as e:
        print(e)
        return "Ошибка, не валидные значения"


print(get_json(json_input))
