# Osmo360 Bluetooth Controller

This project provides a small Python client to connect to a **DJI Osmo Action 360** (or compatible device) over Bluetooth, send basic control commands, and push GPS data to the camera.

## Features

- Connect to the camera via Bluetooth (BLE)
- Handle DJI R SDK–style protocol frames (CRC16/CRC32, framing, parsing)
- Set camera mode (e.g. `PANO_PHOTO`, `PANO_VIDEO`, etc.)
- Start/stop video recording
- Trigger a still image (`grabImage`)
- Subscribe to camera status notifications
- Send GPS data (position, speed, accuracy, satellite count, etc.) to the camera

## Requirements

- Python 3.9+ (recommended)
- Bluetooth Low Energy (BLE) support on the host machine
- Python packages:
  - `bleak`

## Install dependencies:

```
pip install bleak
```

## Configuration

The following constants in Osmo360 may need to be adapted to your setup:

```
TARGET_NAME = "Osmo360-64B3" # BLE name of the camera
LOCAL_MAC = "38-34-56-78-9A-BC" # MAC address of your controller device (as seen by the camera)
```

If your camera broadcasts with a different name, or you want to simulate another controller MAC, adjust these values accordingly.

## Usage

The main entry point is main() at the bottom of the script.
It demonstrates the following workflow:

- Create a GPSData instance with default values.
- Connect to the camera using the async context manager.
- Set the camera mode to PANO_PHOTO.
- Send GPS data to the camera.
- Trigger a single image capture.
- Disconnect.

## Example Flow (from main())

```
async def main():

    gpsdata = GPSData()

    async with Osmo360() as osmo:
        print('connected')
        await asyncio.sleep(2)

        print('set gps')
        await osmo.setMode(CameraMode.PANO_PHOTO)
        await asyncio.sleep(5)

        print('gps')
        await osmo.setGPSData(gpsdata)
        await asyncio.sleep(5)

        await osmo.grabImage()
        await asyncio.sleep(3)

    print('finished')
```

## Notes

- The BLE protocol and command set are reverse-engineered/undocumented and may change with firmware updates.
- Error handling and reconnection logic are intentionally minimal and may need to be hardened for production use.
- Make sure Bluetooth is enabled and the camera is in a state where it is discoverable and accepts controller connections.
