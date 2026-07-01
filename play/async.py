import asyncio

# chef analogy


async def boil_water():
    print('starting to boil water')
    await asyncio.sleep(5)
    print('water boiled to perfect taste')
    return "hot water"


async def chop_carrots():
    print('starting to chop the carrot')
    await asyncio.sleep(10)
    print('finished chopping the carrot')
    return "chopped carrots"


async def main():
    # start task
    water_task = asyncio.create_task(boil_water())
    carrot_task = asyncio.create_task(chop_carrots())

    water = await water_task
    carrot = await carrot_task

    # note this below will not work
    carrot = await chop_carrots()

    print(f'done {water} and {carrot}')

asyncio.run(main())
