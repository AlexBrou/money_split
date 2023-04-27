from pydantic import BaseModel

USER_ALEX = "Alex"
USER_JOANA = "Joana"
USER_GONZALO = "Gonzalo"


class Purchase(BaseModel):
    from_user: str
    amount: float


purchases: list[Purchase] = [
    Purchase(from_user=USER_ALEX, amount=10),
    Purchase(from_user=USER_JOANA, amount=2),
    Purchase(from_user=USER_GONZALO, amount=5),
]


total_pot = sum([x.amount for x in purchases])

amount_for_each = total_pot / 3

amount_alex_needs_to_pay = amount_for_each - sum(
    [x.amount for x in purchases if x.from_user == USER_ALEX]
)
amount_joana_needs_to_pay = amount_for_each - sum(
    [x.amount for x in purchases if x.from_user == USER_JOANA]
)
amount_gonzalo_needs_to_pay = amount_for_each - sum(
    [x.amount for x in purchases if x.from_user == USER_GONZALO]
)

print(0)
