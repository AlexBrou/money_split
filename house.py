from pulp import (
    LpProblem,
    LpMinimize,
    LpVariable,
    LpInteger,
    LpContinuous,
    LpStatusOptimal,
)


SMALL_O = 0.00001

people: tuple[str, float] = [
    ["mishel", -110],
    ["alex", -110],
    ["andre", -941],
    ["gonzalo", 833],
    ["lina", 328],
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
