from pulp import (
    LpProblem,
    LpMinimize,
    LpVariable,
    LpInteger,
    LpContinuous,
    LpStatusOptimal,
)

balances: dict[str, int] = {
    "alex": 0,
    "joana": 0,
    "lina": 0,
    "mischel": 0,
    "gonzalo": 0,
    "andre": 0,
}


expenses: list[tuple[int, str, str, str]] = [
    (12, "alex", "kitchen supplies", "everyone"),
    (10, "joana", "bathroom supplies", "everyone but gonzalo"),
    (10, "lina", "barbecue", "everyone but andre"),
]


balances["alex"] = 10 - 2 - 2  # = 6
balances["joana"] = -2 + 8 - 2  # = 4
balances["lina"] = -2 - 2 + 8  # = 4
balances["mischel"] = -2 - 2 - 2  # = -6
balances["gonzalo"] = -2 - 0 - 2  # = -4
balances["andre"] = -2 - 2 - 0  # = -4


SMALL_O = 0.00001

people: tuple[str, float] = [
    ["alex", 6],
    ["joana", 4],
    ["lina", 4],
    ["mishel", -6],
    ["gonzalo", -4],
    ["andre", -4],
]


assert sum([x[1] for x in people]) == 0


problem = LpProblem("who pays who", LpMinimize)

who_pays_who_variables: dict[str, LpVariable] = {}
how_much_who_pays_who_variables: dict[str, LpVariable] = {}

for person_name, _ in people:
    for another_person_name, _ in people:
        if person_name == another_person_name:
            continue

        who_pays_who_var = LpVariable(
            f"who_pays_who_{person_name}_{another_person_name}",
            lowBound=0,
            upBound=1,
            cat=LpInteger,
        )

        who_pays_who_variables[(person_name, another_person_name)] = who_pays_who_var

        how_much_who_pays_who_var = LpVariable(
            f"how_much_who_pays_who_{person_name}_{another_person_name}",
            lowBound=0,
            upBound=None,
            cat=LpContinuous,
        )

        how_much_who_pays_who_variables[
            (person_name, another_person_name)
        ] = how_much_who_pays_who_var

        problem += who_pays_who_var >= how_much_who_pays_who_var * SMALL_O

for person, amount in people:
    if amount < 0:
        this_person_how_much_vars = []

        for var_key in how_much_who_pays_who_variables.keys():
            from_person, _ = var_key
            if from_person == person:
                this_person_how_much_vars.append(
                    how_much_who_pays_who_variables[var_key]
                )

        problem += sum(this_person_how_much_vars) == abs(amount)
    elif amount > 0:
        this_person_how_much_vars = []

        for var_key in how_much_who_pays_who_variables.keys():
            _, to_person = var_key
            if to_person == person:
                this_person_how_much_vars.append(
                    how_much_who_pays_who_variables[var_key]
                )

        problem += sum(this_person_how_much_vars) == abs(amount)

problem.objective = sum(who_pays_who_variables.values())


status = problem.solve()

assert status == LpStatusOptimal

for vvar in who_pays_who_variables.values():
    if vvar.varValue == 0:
        continue
    print(f"{vvar}  ---  {vvar.varValue}")

for vvar in how_much_who_pays_who_variables.values():
    if vvar.varValue == 0:
        continue
    print(f"{vvar}  ---  {vvar.varValue}")
