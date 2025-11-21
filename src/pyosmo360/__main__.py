# __main__.py
import asyncio
from pyosmo360 import osmo360

async def main():

    async with osmo360.Osmo360("Osmo360-64B3") as osmo:
        print('connected')
        await asyncio.sleep(2)
        await osmo.setMode(osmo360.CameraMode.PANO_PHOTO)
        await asyncio.sleep(5)
        await osmo.grabImage()

    print('finished')


if __name__ == "__main__":
    asyncio.run(main())