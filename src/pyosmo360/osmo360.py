import asyncio
from enum import Enum
import struct
from datetime import datetime
import random
from typing import Optional
from bleak import BleakScanner, BleakClient


class CameraMode(Enum):
    PANO_VIDEO = 0x38
    HYPERLAPSE = 0x3A
    SELFIE = 0x3C
    PANO_PHOTO = 0x3F
    BOOST_VIDEO = 0x41
    VORTEX = 0x43
    PANO_SUPER_NIGHT = 0x44
    SINGLE_LENS_SUPER_NIGHT = 0x4A
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class ViewStatus(Enum):
    SCREEN_OFF = 0x00
    LIVE_STREAMING = 0x01
    PLAYBACK = 0x02
    PHOTO_OR_RECORDING = 0x03
    PRE_RECORDING = 0x05
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class VideoResolution(Enum):
    RES_1080P = 10
    RES_4K = 16
    RES_27K = 45
    RES_1080P_9_16 = 66
    RES_27K_4_3 = 95
    RES_4K_4_3 = 103
    RES_4K_9_16 = 109
    RES_UW_30MP = 4
    RES_W_20MP = 3
    RES_STD_12MP = 2
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class FPSIdx(Enum):
    FPS_24 = 1
    FPS_25 = 2
    FPS_30 = 3
    FPS_48 = 4
    FPS_50 = 5
    FPS_60 = 6
    FPS_100 = 10
    FPS_120 = 7
    FPS_200 = 19
    FPS_240 = 8
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class EISMode(Enum):
    OFF = 0
    RS = 1
    HS = 2
    RS_P = 3
    HB = 4
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class PhotoRatio(Enum):
    RATIO_4_3 = 0
    RATIO_16_9 = 1
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class UserMode(Enum):
    GENERAL = 0
    CUSTOM_1 = 1
    CUSTOM_2 = 2
    CUSTOM_3 = 3
    CUSTOM_4 = 4
    CUSTOM_5 = 5
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class PowerMode(Enum):
    NORMAL = 0
    SLEEP = 3
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class TempOver(Enum):
    NORMAL = 0
    WARNING = 1
    TOO_HIGH = 2
    OVERHEAT = 3
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class GPSData:

    def __init__(self):

        now = datetime.now()
        self._year_month_day: int = now.year * 10000 + now.month * 100 + now.day
        self._hour_minute_second: int = (now.hour + 8) * 10000 + now.minute * 100 + now.second
        self._gps_longitude: int = int(47.0 * 10e6)
        self._gps_latitude: int = int(7.0 * 10e6)
        self._height: int = 250 * 1000        # mm
        self._speed_to_north: float = 0.0     # cm/s
        self._speed_to_east: float = 0.0      # cm/s
        self._speed_to_wnward: float = 0.0    # cm/s
        self._vertical_accuracy_estimate: int = 0   # mm
        self._horizontal_accuracy_estimate: int = 0 # mm
        self._speed_accuracy_estimate: int = 0      # mm
        self._satellite_number: int = 0

    @property
    def year_month_day(self):
        return self._year_month_day

    @year_month_day.setter
    def year_month_day(self, dt: datetime):
        self._year_month_day = dt.year * 10000 + dt.month * 100 + dt.day

    @property
    def hour_minute_second(self):
        return self._hour_minute_second

    @hour_minute_second.setter
    def hour_minute_second(self, dt: datetime):
        self._hour_minute_second = (dt.hour + 8) * 10000 + dt.minute * 100 + dt.second

    @property
    def gps_longitude(self):
        return self._gps_longitude / 10e6

    @gps_longitude.setter
    def gps_longitude(self, value: float):
        self._gps_longitude = int(value * 10e6)

    @property
    def gps_latitude(self):
        return self._gps_latitude / 10e6

    @gps_latitude.setter
    def gps_latitude(self, value: float):
        self._gps_latitude = int(value * 10e6)

    def toData(self):
        bytes_ = struct.pack('<i', self._year_month_day)
        bytes_ += struct.pack('<i', self._hour_minute_second)
        bytes_ += struct.pack('<i', self._gps_longitude)
        bytes_ += struct.pack('<i', self._gps_latitude)
        bytes_ += struct.pack('<i', self._height)
        bytes_ += struct.pack('<f', self._speed_to_north)
        bytes_ += struct.pack('<f', self._speed_to_east)
        bytes_ += struct.pack('<f', self._speed_to_wnward)
        bytes_ += struct.pack('<I', self._vertical_accuracy_estimate)
        bytes_ += struct.pack('<I', self._horizontal_accuracy_estimate)
        bytes_ += struct.pack('<I', self._speed_accuracy_estimate)
        bytes_ += struct.pack('<I', self._satellite_number)
        return bytes_


class CameraStatus:

    camera_mode: CameraMode = CameraMode.PANO_VIDEO
    view_status: ViewStatus = ViewStatus.LIVE_STREAMING
    video_resolution: VideoResolution = VideoResolution.RES_1080P
    fps_idx: FPSIdx = FPSIdx.FPS_24
    eis_mode: EISMode = EISMode.HB
    record_time: int = -1
    fov_type: int = -1
    photo_ratio: PhotoRatio = PhotoRatio.RATIO_4_3
    real_time_countdown: int = -1
    timelaps_interval: int = -1
    timelaps_duration: int = -1
    remain_capacity: int = -1
    remain_photo_num: int = -1
    remain_time: int = -1
    user_mode: UserMode = UserMode.GENERAL
    power_mode: PowerMode = PowerMode.NORMAL
    temp_over: TempOver = TempOver.NORMAL
    photo_countdown_ms: float = -1
    loop_record_sends: int = -1
    camera_bat_percentage: int = -1
    data: bytearray

    def __init__(self):
        pass

    def parseFromData(self, data):
        self.camera_mode = CameraMode(data[0])
        self.view_status = ViewStatus(data[1])
        self.video_resolution = VideoResolution(data[2])
        self.fps_idx = FPSIdx(data[3])
        self.eis_mode = EISMode(data[4])
        self.record_time = struct.unpack('<H', data[5:7])[0]
        self.photo_ratio = PhotoRatio(data[8])
        self.real_time_countdown = struct.unpack('<H', data[9:11])[0]
        self.timelaps_interval = struct.unpack('<H', data[11:13])[0]
        self.timelaps_duration = struct.unpack('<H', data[13:15])[0]
        self.remain_capacity = struct.unpack('<I', data[15:19])[0]
        self.remain_photo_num = struct.unpack('<I', data[19:23])[0]
        self.remain_time = struct.unpack('<I', data[23:27])[0]
        self.user_mode = UserMode(data[28])
        self.power_mode = PowerMode(data[29])
        self.temp_over = TempOver(data[30])
        self.photo_countdown_ms = struct.unpack('<I', data[31:35])[0]
        self.loop_record_sends = struct.unpack('<H', data[35:37])[0]
        self.camera_bat_percentage = data[37]
        self.data = data

    def toData(self):
        pass

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        s = ''
        for attribute, value in self.__dict__.items():
            s += " " + attribute + " : " + str(value)
        return s


class Osmo360:

    client = None
    notification_received = asyncio.Event()
    response_received = asyncio.Event()
    last_notification_data = None

    connection_request_received = asyncio.Event()
    last_connection_request = None
    camera_state = None

    # Bluetooth configuration
    #TARGET_NAME = "Osmo360-64B3"
    SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
    WRITE_UUID = "0000fff5-0000-1000-8000-00805f9b34fb"
    NOTIFY_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"
    #LOCAL_MAC = "38-34-56-78-9A-BC"

    CTR_DEVICE_ID = 0x01020304  # DJI GPS Controller

    camera_name = ''
    cameraStatus: CameraStatus
    verbose: bool = False
    cameraStatusCallbacks = []

    def __init__(self, camera_name, local_mac = "01-02-03-04-05-06"):
        self.camera_name = camera_name
        self.local_mac = local_mac

    def is_connected(self):
        pass

    async def _connect_bt(self):
        """Connect camera via Bluetooth"""
        if self.verbose: print("Starting Bluetooth scan...")
        devices = await BleakScanner.discover(2)

        target_device = None
        for d in devices:
            if d.name and self.camera_name in d.name:
                if self.verbose: print(f"Target device found: {d.name} ({d.address})")
                target_device = d
                break

        if not target_device:
            raise Exception("DJI Osmo Action device not found")

        if self.verbose: print(f"Connecting to device: {target_device.address}")
        self.client = BleakClient(target_device.address)
        await self.client.connect()
        if self.verbose: print("Bluetooth connection established")

        # Enable notifications
        await self.client.start_notify(self.NOTIFY_UUID, self._notification_handler)
        if self.verbose: print("Notifications enabled")

    async def connect(self):
        """Send connection request and handle handshake"""

        if not self.client or not self.client.is_connected:
            await self._connect_bt()

        if self.verbose: print("Sending connection request...")

        verify_code = random.randint(0, 9999)
        is_first_pairing = False

        payload = struct.pack(
            "<IB16sIBBH4s",
            self.CTR_DEVICE_ID,
            6,
            self._parse_mac_address(self.local_mac) + b'\x00' * 10,
            0,
            0,
            1 if is_first_pairing else 0,
            verify_code,
            b'\x00' * 4
        )

        frame = await self.send_dji_command(0x00, 0x19, payload)

        if not frame:
            print("No response received for connection request")
            return False

        try:
            if self.verbose:
                if self.verbose: print(f"Full response frame received: {frame}")

            if frame['cmd_set'] != 0x00 or frame['cmd_id'] != 0x19:
                if self.verbose: print("Response frame does not belong to connection request")
                return False

            if frame['frame_type'] != 1:
                if self.verbose: print("Response frame is not of response type")
                return False

            if len(frame['data']) < 5:
                if self.verbose: print("Response data too short")
                return False

            self.device_id = int.from_bytes(frame['data'][0:4], 'little')
            ret_code = frame['data'][4]

            if self.verbose: print(f"Camera response - Device ID: 0x{self.device_id:04X}, return code: {ret_code}")

            if ret_code != 0x00:
                if self.verbose: print(f"Connection request rejected, error code: {ret_code}")
                return False

            if self.verbose: print("Waiting for connection request from camera...")
            self.notification_received.clear()
            try:
                await asyncio.wait_for(self.notification_received.wait(), 10)

                if self.last_notification_data:
                    frame = self.last_notification_data
                    if frame['cmd_set'] == 0x00 and frame['cmd_id'] == 0x19 and frame['frame_type'] == 0:
                        if len(frame['data']) >= 29:
                            cam_verify_mode = frame['data'][26]
                            cam_verify_data = int.from_bytes(frame['data'][27:29], 'little')

                            if self.verbose: print(
                                f"Camera connection request - verification mode: {cam_verify_mode}, "
                                f"verification result: {cam_verify_data}"
                            )

                            if cam_verify_mode == 2:
                                if cam_verify_data == 0:
                                    if self.verbose: print("Camera allows connection")
                                    ack_payload = struct.pack("<IB4s", 0x12345678, 0x00, b'\x00\x00\x00\x00')
                                    await self.send_dji_command(0x00, 0x19, ack_payload, is_response=True)
                                    return self.device_id
                                else:
                                    if self.verbose: print("Camera denies connection")
                                    if self.client: await self.client.disconnect()
                                    return False
            except asyncio.TimeoutError:
                print("Timeout while waiting for camera connection request")
                return False

        except Exception as e:
            print(f"Error parsing connection response: {e}")
            return False

    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()

    async def _notification_handler(self, sender, data):
        """Process notifications from the camera"""

        try:
            frame = self.parse_dji_frame(data)
            if self.verbose:
                if self.verbose: print(f"Full protocol frame received: {frame}")

            if frame['frame_type'] == 1:
                self.last_response_frame = frame
                self.response_received.set()
            else:
                self.last_notification_data = frame
                self.notification_received.set()

                if frame['cmd_set'] == 29 and frame['cmd_id'] == 2:
                    # camera status
                    self.cameraStatus = CameraStatus()
                    self.cameraStatus.parseFromData(frame['data'])
                    for cb in self.cameraStatusCallbacks:
                        cb(self.cameraStatus)

        except ValueError as e:
            if self.verbose:
                print(e)
        except Exception as e:
            print(f"Error parsing notification: {e}")

    def subscribeKeyPress(self, callback):
        # todo
        pass

    def unsubscribeKeyPress(self, callback):
        # todo
        pass

    async def setMode(self, mode: CameraMode):
        if self.verbose: print('setMode to: ' + mode.name)
        ack_payload = struct.pack("<IB4s", self.device_id, mode.value, b'\x00\x00\x00\x00')
        resp = await self.send_dji_command(0x1D, 0x04, ack_payload, wait_for_response=True)
        return resp is not None and resp['data'] == 0x00

    async def startRecording(self):
        if self.verbose: print('startRecording')
        ack_payload = struct.pack("<IB4s", self.device_id, 0x00, b'\x00\x00\x00\x00')
        resp = await self.send_dji_command(0x1D, 0x03, ack_payload, wait_for_response=True)
        return resp is not None and resp['data'] == 0x00

    async def stopRecording(self):
        if self.verbose: print('stopRecording')
        ack_payload = struct.pack("<IB4s", self.device_id, 0x01, b'\x00\x00\x00\x00')
        resp = await self.send_dji_command(0x1D, 0x03, ack_payload, wait_for_response=True)
        return resp is not None and resp['data'] == 0x00

    async def grabImage(self):
        if self.verbose: print('grab image')
        ack_payload = struct.pack("<IB4s", self.device_id, 0x00, b'\x00\x00\x00\x00')
        resp = await self.send_dji_command(0x1D, 0x03, ack_payload, wait_for_response=True)
        return resp is not None and resp['data'] == 0x00

    '''
    doesn't work?
    async def deviceRestart(self):
        ack_payload = struct.pack("<I4s", self.device_id, b'\x00\x00\x00\x00')
        resp = await self.send_dji_command(0x00, 0x16, ack_payload, wait_for_response=True)
        return resp
    '''

    async def subscribeCameraStatus(self, callback):
        ack_payload = struct.pack("<BB4s", 0x02, 0x14, b'\x00\x00\x00\x00')
        resp = await self.send_dji_command(0x1D, 0x05, ack_payload, wait_for_response=True)
        self.cameraStatusCallbacks.append(callback)
        return resp

    async def unSubscribeCameraStatus(self, callback):
        self.cameraStatusCallbacks.remove(callback)
        if len(self.cameraStatusCallbacks) == 0:
            ack_payload = struct.pack("<BB4s", 0x00, 0x14, b'\x00\x00\x00\x00')
            resp = await self.send_dji_command(0x1D, 0x05, ack_payload, wait_for_response=True)

    async def setGPSData(self, gpsdata: GPSData):
        ack_payload = gpsdata.toData()
        resp = await self.send_dji_command(0x00, 0x17, ack_payload, wait_for_response=True)
        return resp

    async def __aenter__(self):
        await self.connect()
        return self

    async def __await__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def send_dji_command(self, cmd_set, cmd_id, payload, wait_for_response=True, timeout=5, is_response=False)  -> Optional[dict]:
        """Send DJI command and wait for response"""

        if not self.client or not self.client.is_connected:
            raise Exception("Bluetooth not connected")

        if is_response:
            wait_for_response = False

        self.last_response_frame = None
        frame = self.build_dji_frame(cmd_set, cmd_id, payload, is_response, ack_type=1)
        if self.verbose: print(f"Sending DJI command: {frame.hex()}")
        await self.client.write_gatt_char(self.WRITE_UUID, frame, response=True)

        if self.last_response_frame:
            return self.last_response_frame

        if wait_for_response:
            if self.verbose: print("Waiting for response...")
            self.response_received.clear()
            try:
                await asyncio.wait_for(self.response_received.wait(), timeout)
                return self.last_response_frame
            except asyncio.TimeoutError:
                print("Timeout while waiting for response")
                return None
        return None

    def build_dji_frame(self, cmd_set, cmd_id, payload, is_response=False, ack_type=1):
        """
        Create DJI R SDK protocol frame

        Parameters:
            cmd_set: command set ID
            cmd_id: command ID
            payload: payload (bytes)
            is_response: whether this is a response frame (False = command frame, True = response frame)
            ack_type: acknowledgment type
                0 - no response required
                1 - response desired, but not mandatory
                2 - response required (2–31 are mandatory)
        """

        # Create DATA part
        data = bytes([cmd_set, cmd_id]) + payload

        # Create CmdType byte
        cmd_type_byte = 0x00
        # Set acknowledgment type [4:0]
        cmd_type_byte |= (ack_type & 0x1F)  # only lower 5 bits
        # Set frame type [5]
        if is_response:
            cmd_type_byte |= 0x20  # set bit 5 to 1 for response frame
        # [7:6] reserved, stay 0

        # Create frame header
        length = 12 + len(data) + 4  # total length from SOF to CRC32
        ver_length = (0 << 10) | (length & 0x03FF)  # version number 0
        ver_length_bytes = ver_length.to_bytes(2, 'little')

        frame_header = bytes([
            0xAA,  # SOF
            ver_length_bytes[0], ver_length_bytes[1],  # Ver/Length
            cmd_type_byte,  # CmdType (contains acknowledgment and frame type)
            0x00,  # ENC (not encrypted)
            0x00, 0x00, 0x00,  # RES (reserved)
            0x01, 0x00,  # SEQ (sequence number, fixed 1 here)
        ])

        # Calculate CRC16 (SOF to SEQ)
        crc16 = self._ccrc16(frame_header)
        frame_header += crc16.to_bytes(2, 'little')

        # Complete frame (SOF to DATA)
        full_frame = frame_header + data

        # Calculate CRC32 (SOF to DATA)
        crc32 = self._ccrc32(full_frame)
        full_frame += crc32.to_bytes(4, 'little')

        return full_frame

    def parse_dji_frame(self, data) -> dict:
        """Parse DJI R SDK protocol frame"""
        if len(data) < 16:  # minimum length (SOF to CRC32)
            raise ValueError("Frame data is too short")

        if self.verbose:
            print(data.hex())

        # Check SOF
        if data[0] != 0xAA:
            raise ValueError("Invalid frame header (SOF)")

        # Analyze length field (Ver/Length)
        ver_length = int.from_bytes(data[1:3], 'little')
        version = (ver_length >> 10) & 0x3F
        length = ver_length & 0x3FF

        # Check if length matches
        if len(data) != length:
            raise ValueError(
                f"Frame length mismatch, declared: {length}, actual: {len(data)}"
            )

        # Analyze CmdType
        cmd_type = data[3]
        frame_type = (cmd_type >> 5) & 0x01  # 0 = command frame, 1 = response frame
        ack_type = cmd_type & 0x1F

        # Analyze ENC
        enc = data[4]

        # Analyze SEQ
        seq = int.from_bytes(data[8:10], 'little')

        # Check CRC16 (SOF to SEQ)
        crc16_calculated = self._ccrc16(data[0:10])
        crc16_received = int.from_bytes(data[10:12], 'little')
        if crc16_calculated != crc16_received:
            raise ValueError(
                f"CRC16 check failed, calculated:{crc16_calculated:04X}, received:{crc16_received:04X}"
            )

        # Extract DATA area
        data_start = 12
        data_end = length - 4  # subtract CRC32 (4 bytes)
        data_payload = data[data_start:data_end]

        # Check CRC32 (SOF to DATA)
        crc32_calculated = self._ccrc32(data[0:data_end])
        crc32_received = int.from_bytes(data[data_end:length], 'little')
        if crc32_calculated != crc32_received:
            raise ValueError(
                f"CRC32 check failed, calculated:{crc32_calculated:08X}, received:{crc32_received:08X}"
            )

        # Analyze DATA area CmdSet and CmdID
        if len(data_payload) < 2:
            raise ValueError("DATA section too short")
        cmd_set = data_payload[0]
        cmd_id = data_payload[1]
        actual_data = data_payload[2:]

        return {
            'version': version,
            'length': length,
            'frame_type': frame_type,
            'ack_type': ack_type,
            'enc': enc,
            'seq': seq,
            'crc16': crc16_received,
            'crc32': crc32_received,
            'cmd_set': cmd_set,
            'cmd_id': cmd_id,
            'data': actual_data
        }

    DJI_CRC16_TABLE = [
        0x0000, 0xc0c1, 0xc181, 0x0140, 0xc301, 0x03c0, 0x0280, 0xc241,
        0xc601, 0x06c0, 0x0780, 0xc741, 0x0500, 0xc5c1, 0xc481, 0x0440,
        0xcc01, 0x0cc0, 0x0d80, 0xcd41, 0x0f00, 0xcfc1, 0xce81, 0x0e40,
        0x0a00, 0xcac1, 0xcb81, 0x0b40, 0xc901, 0x09c0, 0x0880, 0xc841,
        0xd801, 0x18c0, 0x1980, 0xd941, 0x1b00, 0xdbc1, 0xda81, 0x1a40,
        0x1e00, 0xdec1, 0xdf81, 0x1f40, 0xdd01, 0x1dc0, 0x1c80, 0xdc41,
        0x1400, 0xd4c1, 0xd581, 0x1540, 0xd701, 0x17c0, 0x1680, 0xd641,
        0xd201, 0x12c0, 0x1380, 0xd341, 0x1100, 0xd1c1, 0xd081, 0x1040,
        0xf001, 0x30c0, 0x3180, 0xf141, 0x3300, 0xf3c1, 0xf281, 0x3240,
        0x3600, 0xf6c1, 0xf781, 0x3740, 0xf501, 0x35c0, 0x3480, 0xf441,
        0x3c00, 0xfcc1, 0xfd81, 0x3d40, 0xff01, 0x3fc0, 0x3e80, 0xfe41,
        0xfa01, 0x3ac0, 0x3b80, 0xfb41, 0x3900, 0xf9c1, 0xf881, 0x3840,
        0x2800, 0xe8c1, 0xe981, 0x2940, 0xeb01, 0x2bc0, 0x2a80, 0xea41,
        0xee01, 0x2ec0, 0x2f80, 0xef41, 0x2d00, 0xedc1, 0xec81, 0x2c40,
        0xe401, 0x24c0, 0x2580, 0xe541, 0x2700, 0xe7c1, 0xe681, 0x2640,
        0x2200, 0xe2c1, 0xe381, 0x2340, 0xe101, 0x21c0, 0x2080, 0xe041,
        0xa001, 0x60c0, 0x6180, 0xa141, 0x6300, 0xa3c1, 0xa281, 0x6240,
        0x6600, 0xa6c1, 0xa781, 0x6740, 0xa501, 0x65c0, 0x6480, 0xa441,
        0x6c00, 0xacc1, 0xad81, 0x6d40, 0xaf01, 0x6fc0, 0x6e80, 0xae41,
        0xaa01, 0x6ac0, 0x6b80, 0xab41, 0x6900, 0xa9c1, 0xa881, 0x6840,
        0x7800, 0xb8c1, 0xb981, 0x7940, 0xbb01, 0x7bc0, 0x7a80, 0xba41,
        0xbe01, 0x7ec0, 0x7f80, 0xbf41, 0x7d00, 0xbdc1, 0xbc81, 0x7c40,
        0xb401, 0x74c0, 0x7580, 0xb541, 0x7700, 0xb7c1, 0xb681, 0x7640,
        0x7200, 0xb2c1, 0xb381, 0x7340, 0xb101, 0x71c0, 0x7080, 0xb041,
        0x5000, 0x90c1, 0x9181, 0x5140, 0x9301, 0x53c0, 0x5280, 0x9241,
        0x9601, 0x56c0, 0x5780, 0x9741, 0x5500, 0x95c1, 0x9481, 0x5440,
        0x9c01, 0x5cc0, 0x5d80, 0x9d41, 0x5f00, 0x9fc1, 0x9e81, 0x5e40,
        0x5a00, 0x9ac1, 0x9b81, 0x5b40, 0x9901, 0x59c0, 0x5880, 0x9841,
        0x8801, 0x48c0, 0x4980, 0x8941, 0x4b00, 0x8bc1, 0x8a81, 0x4a40,
        0x4e00, 0x8ec1, 0x8f81, 0x4f40, 0x8d01, 0x4dc0, 0x4c80, 0x8c41,
        0x4400, 0x84c1, 0x8581, 0x4540, 0x8701, 0x47c0, 0x4680, 0x8641,
        0x8201, 0x42c0, 0x4380, 0x8341, 0x4100, 0x81c1, 0x8081, 0x4040
    ]

    DJI_CRC32_TABLE = [
        0x00000000, 0x77073096, 0xee0e612c, 0x990951ba, 0x076dc419, 0x706af48f, 0xe963a535, 0x9e6495a3,
        0x0edb8832, 0x79dcb8a4, 0xe0d5e91e, 0x97d2d988, 0x09b64c2b, 0x7eb17cbd, 0xe7b82d07, 0x90bf1d91,
        0x1db71064, 0x6ab020f2, 0xf3b97148, 0x84be41de, 0x1adad47d, 0x6ddde4eb, 0xf4d4b551, 0x83d385c7,
        0x136c9856, 0x646ba8c0, 0xfd62f97a, 0x8a65c9ec, 0x14015c4f, 0x63066cd9, 0xfa0f3d63, 0x8d080df5,
        0x3b6e20c8, 0x4c69105e, 0xd56041e4, 0xa2677172, 0x3c03e4d1, 0x4b04d447, 0xd20d85fd, 0xa50ab56b,
        0x35b5a8fa, 0x42b2986c, 0xdbbbc9d6, 0xacbcf940, 0x32d86ce3, 0x45df5c75, 0xdcd60dcf, 0xabd13d59,
        0x26d930ac, 0x51de003a, 0xc8d75180, 0xbfd06116, 0x21b4f4b5, 0x56b3c423, 0xcfba9599, 0xb8bda50f,
        0x2802b89e, 0x5f058808, 0xc60cd9b2, 0xb10be924, 0x2f6f7c87, 0x58684c11, 0xc1611dab, 0xb6662d3d,
        0x76dc4190, 0x01db7106, 0x98d220bc, 0xefd5102a, 0x71b18589, 0x06b6b51f, 0x9fbfe4a5, 0xe8b8d433,
        0x7807c9a2, 0x0f00f934,         0x9609a88e, 0xe10e9818, 0x7f6a0dbb, 0x086d3d2d, 0x91646c97, 0xe6635c01,
        0x6b6b51f4, 0x1c6c6162, 0x856530d8, 0xf262004e, 0x6c0695ed, 0x1b01a57b, 0x8208f4c1, 0xf50fc457,
        0x65b0d9c6, 0x12b7e950, 0x8bbeb8ea, 0xfcb9887c, 0x62dd1ddf, 0x15da2d49, 0x8cd37cf3, 0xfbd44c65,
        0x4db26158, 0x3ab551ce, 0xa3bc0074, 0xd4bb30e2, 0x4adfa541, 0x3dd895d7, 0xa4d1c46d, 0xd3d6f4fb,
        0x4369e96a, 0x346ed9fc, 0xad678846, 0xda60b8d0, 0x44042d73, 0x33031de5, 0xaa0a4c5f, 0xdd0d7cc9,
        0x5005713c, 0x270241aa, 0xbe0b1010, 0xc90c2086, 0x5768b525, 0x206f85b3, 0xb966d409, 0xce61e49f,
        0x5edef90e, 0x29d9c998, 0xb0d09822, 0xc7d7a8b4, 0x59b33d17, 0x2eb40d81, 0xb7bd5c3b, 0xc0ba6cad,
        0xedb88320, 0x9abfb3b6, 0x03b6e20c, 0x74b1d29a, 0xead54739, 0x9dd277af, 0x04db2615, 0x73dc1683,
        0xe3630b12, 0x94643b84, 0x0d6d6a3e, 0x7a6a5aa8, 0xe40ecf0b, 0x9309ff9d, 0x0a00ae27, 0x7d079eb1,
        0xf00f9344, 0x8708a3d2, 0x1e01f268, 0x6906c2fe, 0xf762575d, 0x806567cb, 0x196c3671, 0x6e6b06e7,
        0xfed41b76, 0x89d32be0, 0x10da7a5a, 0x67dd4acc, 0xf9b9df6f, 0x8ebeeff9, 0x17b7be43, 0x60b08ed5,
        0xd6d6a3e8, 0xa1d1937e, 0x38d8c2c4, 0x4fdff252, 0xd1bb67f1, 0xa6bc5767, 0x3fb506dd, 0x48b2364b,
        0xd80d2bda, 0xaf0a1b4c, 0x36034af6, 0x41047a60, 0xdf60efc3, 0xa867df55, 0x316e8eef, 0x4669be79,
        0xcb61b38c, 0xbc66831a, 0x256fd2a0, 0x5268e236, 0xcc0c7795, 0xbb0b4703, 0x220216b9, 0x5505262f,
        0xc5ba3bbe, 0xb2bd0b28, 0x2bb45a92, 0x5cb36a04, 0xc2d7ffa7, 0xb5d0cf31, 0x2cd99e8b, 0x5bdeae1d,
        0x9b64c2b0, 0xec63f226, 0x756aa39c, 0x026d930a, 0x9c0906a9, 0xeb0e363f, 0x72076785, 0x05005713,
        0x95bf4a82, 0xe2b87a14, 0x7bb12bae, 0x0cb61b38, 0x92d28e9b, 0xe5d5be0d, 0x7cdcefb7, 0x0bdbdf21,
        0x86d3d2d4, 0xf1d4e242, 0x68ddb3f8, 0x1fda836e, 0x81be16cd, 0xf6b9265b, 0x6fb077e1, 0x18b74777,
        0x88085ae6, 0xff0f6a70, 0x66063bca, 0x11010b5c, 0x8f659eff, 0xf862ae69, 0x616bffd3, 0x166ccf45,
        0xa00ae278, 0xd70dd2ee, 0x4e048354, 0x3903b3c2, 0xa7672661, 0xd06016f7, 0x4969474d, 0x3e6e77db,
        0xaed16a4a, 0xd9d65adc, 0x40df0b66, 0x37d83bf0, 0xa9bcae53, 0xdebb9ec5, 0x47b2cf7f, 0x30b5ffe9,
        0xbdbdf21c, 0xcabac28a, 0x53b39330, 0x24b4a3a6, 0xbad03605, 0xcdd70693, 0x54de5729, 0x23d967bf,
        0xb3667a2e, 0xc4614ab8, 0x5d681b02, 0x2a6f2b94, 0xb40bbe37, 0xc30c8ea1, 0x5a05df1b, 0x2d02ef8d
    ]

    def _ccrc16(self, data: bytes, init=0x3AA3) -> int:
        crc = init
        for b in data:
            tbl_idx = (crc ^ b) & 0xFF
            crc = (self.DJI_CRC16_TABLE[tbl_idx] ^ (crc >> 8)) & 0xFFFF
        return crc

    def _ccrc32(self, data: bytes, init=0x00003AA3) -> int:
        crc = init
        for b in data:
            tbl_idx = (crc ^ b) & 0xFF
            crc = (self.DJI_CRC32_TABLE[tbl_idx] ^ (crc >> 8)) & 0xFFFFFFFF
        return crc

    def _parse_mac_address(self, mac_str):
        """Convert MAC address string to byte array"""
        return bytes.fromhex(mac_str.replace(':', '').replace('-', ''))



