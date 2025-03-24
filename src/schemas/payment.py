from pydantic import BaseModel


class PaymentCreate(BaseModel):
    id: int
    price: int
