from Service import Service
from Inventory import Inventory
from Factory import Factory

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    amount = 10
    service = Service()

    product_1 = service.define_product("T1")
    product_2 = service.define_product("T2")
    product_3 = service.define_product("T3")
    product_4 = service.define_product("T4")

    service.define_recipie("R1", product_1, 5, [product_2, product_3])
    service.define_recipie("R2", product_2, 3.5, [])
    service.define_recipie("R3", product_3, 4, [product_4])
    service.define_recipie("R4", product_4, 2, [])

    service.create_machine("M1", [product_4, product_3])
    service.create_machine("M2", [product_2])
    service.create_machine("M3", [product_1])

    factory = Factory(service=service)

    target_inventory = Inventory([service.create_product(name="T1") for _ in range(amount)])

    schedule = factory.create_schedule(target_inventory)

    for task in schedule:
        print(task)

    result = {'SCHEDULE': {},
              "KPI": {}}

    for machine in set(task.selected_machine for task in schedule):
        result['SCHEDULE'][machine.name] = [task for task in schedule if task.selected_machine == machine]
        print('----------------------------------------')
        print(machine)
        for (time, recipie, index) in [(task.time, task.recipie, index) for (index, task) in enumerate(schedule) if
                                       task.selected_machine == machine]:
            print(f"Task no# {index: <4} : {time:<4} - {recipie.get_timer() + time:<4} : {recipie}")

    result['KPI']['PRODUCTS'] = factory.execute(schedule)
    time = max([task.time + task.recipie.timer for task in schedule])
    result['KPI']['TOTAL_TIME'] = time
    usage = 0
    for second in range(0, int(time)):
        usage += len(
            {task.selected_machine for task in schedule if task.time <= second < task.time + task.recipie.timer}) / len(
            service.machines)
    result['KPI']['EFFICIENCY'] = format(usage / time, ".4f")
    print('----------------')
    for kpi in result['KPI'].keys():
        print(f"{kpi}: {result['KPI'][kpi]} ")
    return result


@app.post("/")
async def say_hello(request: Request):
    data = await request.json()
    amount = data.get("amount", 10)
    service = Service()

    product_1 = service.define_product("T1")
    product_2 = service.define_product("T2")
    product_3 = service.define_product("T3")
    product_4 = service.define_product("T4")

    service.define_recipie("R1", product_1, 5, [product_2, product_3])
    service.define_recipie("R2", product_2, 3.5, [])
    service.define_recipie("R3", product_3, 4, [product_4])
    service.define_recipie("R4", product_4, 2, [])

    service.create_machine("M1", [product_4, product_3])
    service.create_machine("M2", [product_2])
    service.create_machine("M3", [product_1])

    factory = Factory(service=service)

    target_inventory = Inventory([service.create_product(name="T1") for _ in range(amount)])

    schedule = factory.create_schedule(target_inventory)

    for task in schedule:
        print(task)

    result = {'SCHEDULE': {},
              "KPI": {}}

    for machine in set(task.selected_machine for task in schedule):
        result['SCHEDULE'][machine.name] = [task for task in schedule if task.selected_machine == machine]
        print('----------------------------------------')
        print(machine)
        for (time, recipie, index) in [(task.time, task.recipie, index) for (index, task) in enumerate(schedule) if
                                       task.selected_machine == machine]:
            print(f"Task no# {index: <4} : {time:<4} - {recipie.get_timer() + time:<4} : {recipie}")

    result['KPI']['PRODUCTS'] = factory.execute(schedule)
    time = max([task.time + task.recipie.timer for task in schedule])
    result['KPI']['TOTAL_TIME'] = time
    usage = 0
    for second in range(0, int(time)):
        usage += len(
            {task.selected_machine for task in schedule if task.time <= second < task.time + task.recipie.timer}) / len(
            service.machines)
    result['KPI']['EFFICIENCY'] = format(usage / time, ".4f")
    print('----------------')
    for kpi in result['KPI'].keys():
        print(f"{kpi}: {result['KPI'][kpi]} ")
    return result
