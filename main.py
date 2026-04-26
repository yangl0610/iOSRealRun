import random
import asyncio

from pymobiledevice3.remote.remote_service_discovery import RemoteServiceDiscoveryService
from pymobiledevice3.services.dvt.instruments.location_simulation import LocationSimulation
from pymobiledevice3.services.dvt.instruments.dvt_provider import DvtProvider

from utils import get_route
from core import simulat_run

async def main(full_address: tuple, loc: list):
    rsd = RemoteServiceDiscoveryService(full_address)
    await rsd.connect()

    async with DvtProvider(rsd) as dvt, LocationSimulation(dvt) as location_simulation:
        while True:
            random_v = 1500/(1000/3-(2*random.random()-1)*15)
            await simulat_run(location_simulation, loc, random_v)
            print("Lap Finished!")

if __name__ == "__main__":

    host = str(input("HOST:"))
    port = int(input("PORT:"))
    full_address = (host, port)
    
    asyncio.run(main(full_address, get_route()))
