"""Python wrapper for HIDAPI library.

This module provides a Python interface to the HIDAPI library for communicating
with HID devices.
"""
import atexit
import ctypes
import enum
from typing import Any, Dict, List, Optional, Union

hid_library_path = 'libhidapi-hidraw.so.0'

try:
    hidapi = ctypes.cdll.LoadLibrary(hid_library_path)
except OSError as exc:
    raise ImportError(f"Unable to load {hid_library_path}") from exc

hidapi.hid_init()
atexit.register(hidapi.hid_exit)


class HIDException(Exception):
    """Exception raised for HID device errors."""


class BusType(enum.Enum):
    """Enumeration of HID device bus types."""

    UNKNOWN = 0x00
    USB = 0x01
    BLUETOOTH = 0x02
    I2C = 0x03
    SPI = 0x04


class DeviceInfo(ctypes.Structure):
    """Structure representing HID device information."""

    def as_dict(self) -> Dict[str, Any]:
        """Convert device info to dictionary format."""
        ret = {}
        for name, _ in self._fields_:
            if name == 'next':
                continue
            ret[name] = getattr(self, name, None)
            if name == 'bus_type':
                ret[name] = BusType(ret[name])
        return ret


DeviceInfo._fields_ = [
    ('path', ctypes.c_char_p),
    ('vendor_id', ctypes.c_ushort),
    ('product_id', ctypes.c_ushort),
    ('serial_number', ctypes.c_wchar_p),
    ('release_number', ctypes.c_ushort),
    ('manufacturer_string', ctypes.c_wchar_p),
    ('product_string', ctypes.c_wchar_p),
    ('usage_page', ctypes.c_ushort),
    ('usage', ctypes.c_ushort),
    ('interface_number', ctypes.c_int),
    ('next', ctypes.POINTER(DeviceInfo)),
    ('bus_type', ctypes.c_int),
]


hidapi.hid_init.argtypes = []
hidapi.hid_init.restype = ctypes.c_int
hidapi.hid_exit.argtypes = []
hidapi.hid_exit.restype = ctypes.c_int
hidapi.hid_enumerate.argtypes = [ctypes.c_ushort, ctypes.c_ushort]
hidapi.hid_enumerate.restype = ctypes.POINTER(DeviceInfo)
hidapi.hid_free_enumeration.argtypes = [ctypes.POINTER(DeviceInfo)]
hidapi.hid_free_enumeration.restype = None
hidapi.hid_open.argtypes = [ctypes.c_ushort, ctypes.c_ushort, ctypes.c_wchar_p]
hidapi.hid_open.restype = ctypes.c_void_p
hidapi.hid_open_path.argtypes = [ctypes.c_char_p]
hidapi.hid_open_path.restype = ctypes.c_void_p
hidapi.hid_write.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
hidapi.hid_write.restype = ctypes.c_int
hidapi.hid_read_timeout.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_int
]
hidapi.hid_read_timeout.restype = ctypes.c_int
hidapi.hid_read.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
hidapi.hid_read.restype = ctypes.c_int
hidapi.hid_close.argtypes = [ctypes.c_void_p]
hidapi.hid_close.restype = None
hidapi.hid_get_manufacturer_string.argtypes = [
    ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_size_t
]
hidapi.hid_get_manufacturer_string.restype = ctypes.c_int
hidapi.hid_get_product_string.argtypes = [
    ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_size_t
]
hidapi.hid_get_product_string.restype = ctypes.c_int
hidapi.hid_get_serial_number_string.argtypes = [
    ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_size_t
]
hidapi.hid_get_serial_number_string.restype = ctypes.c_int
hidapi.hid_get_device_info.argtypes = [ctypes.c_void_p]
hidapi.hid_get_device_info.restype = ctypes.POINTER(DeviceInfo)
hidapi.hid_error.argtypes = [ctypes.c_void_p]
hidapi.hid_error.restype = ctypes.c_wchar_p


def enumerate_devices(vid: int = 0, pid: int = 0) -> List[Dict[str, Any]]:
    """Enumerate HID devices.

    Args:
        vid: Vendor ID to filter by (0 for all)
        pid: Product ID to filter by (0 for all)

    Returns:
        List of device information dictionaries
    """
    ret = []
    info = hidapi.hid_enumerate(vid, pid)
    c = info

    while c:
        ret.append(c.contents.as_dict())
        c = c.contents.next

    hidapi.hid_free_enumeration(info)

    return ret


class Device:
    """HID device interface."""

    def __init__(
        self, 
        vid: Optional[int] = None, 
        pid: Optional[int] = None, 
        serial: Optional[str] = None, 
        path: Optional[bytes] = None
    ) -> None:
        """Initialize HID device.

        Args:
            vid: Vendor ID
            pid: Product ID
            serial: Serial number string
            path: Device path
        """
        if path:
            self.__dev = hidapi.hid_open_path(path)
        elif serial:
            serial = ctypes.create_unicode_buffer(serial)
            self.__dev = hidapi.hid_open(vid, pid, serial)
        elif vid and pid is not None:
            self.__dev = hidapi.hid_open(vid, pid, None)
        else:
            raise ValueError('specify vid/pid or path')

        if not self.__dev:
            raise HIDException('unable to open device')

    def __enter__(self) -> 'Device':
        """Enter context manager.
        
        Returns:
            Self for context management
        """
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        """Exit context manager.
        
        Args:
            exc_type: Exception type
            exc_value: Exception value  
            exc_traceback: Exception traceback
        """
        self.close()

    def __hidcall(self, function: Any, *args: Any, **kwargs: Any) -> Any:
        """Call HID API function with error checking.
        
        Args:
            function: HID API function to call
            *args: Arguments to pass to function
            **kwargs: Keyword arguments to pass to function
            
        Returns:
            Function return value
            
        Raises:
            HIDException: If the HID call fails
        """
        if not self.__dev:
            raise HIDException('device closed')

        ret = function(*args, **kwargs)

        if ret == -1:
            err = hidapi.hid_error(self.__dev)
            raise HIDException(err)
        return ret

    def __readstring(self, function: Any, max_length: int = 255) -> Optional[str]:
        """Read string from HID device using provided function.
        
        Args:
            function: HID API string function to call
            max_length: Maximum string length to read
            
        Returns:
            String value or None if failed
        """
        buf = ctypes.create_unicode_buffer(max_length)
        self.__hidcall(function, self.__dev, buf, max_length)
        return buf.value

    def write(self, data: Union[List[int], bytes]) -> int:
        """Write data to the device.
        
        Args:
            data: Data to write as list of integers or bytes
            
        Returns:
            Number of bytes written
            
        Raises:
            HIDException: If write operation fails
        """
        return self.__hidcall(hidapi.hid_write, self.__dev, data, len(data))

    def read(self, size: int, timeout: Optional[int] = None) -> List[int]:
        """Read data from the device.
        
        Args:
            size: Number of bytes to read
            timeout: Timeout in milliseconds (None for blocking)
            
        Returns:
            List of integers representing the read data
            
        Raises:
            HIDException: If read operation fails
        """
        data = ctypes.create_string_buffer(size)

        if timeout is None:
            size = self.__hidcall(hidapi.hid_read, self.__dev, data, size)
        else:
            size = self.__hidcall(
                hidapi.hid_read_timeout, self.__dev, data, size, timeout)

        return data.raw[:size]

    def close(self) -> None:
        """Close the device.
        
        Closes the HID device connection and releases resources.
        """
        if self.__dev:
            hidapi.hid_close(self.__dev)
            self.__dev = None

    @property
    def manufacturer(self) -> Optional[str]:
        """Get manufacturer string.
        
        Returns:
            Manufacturer name or None if unavailable
        """
        return self.__readstring(hidapi.hid_get_manufacturer_string)

    @property
    def product(self) -> Optional[str]:
        """Get product string.
        
        Returns:
            Product name or None if unavailable
        """
        return self.__readstring(hidapi.hid_get_product_string)

    @property
    def serial(self) -> Optional[str]:
        """Get serial number string.
        
        Returns:
            Serial number or None if unavailable
        """
        return self.__readstring(hidapi.hid_get_serial_number_string)

    def get_device_info(self) -> Dict[str, Any]:
        """Get device information.
        
        Returns:
            Dictionary containing device information
        """
        info = hidapi.hid_get_device_info(self.__dev)
        return info.contents.as_dict()
