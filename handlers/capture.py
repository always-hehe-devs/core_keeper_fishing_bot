import numpy as np
from ctypes import windll
import win32gui
import win32ui


class CaptureScreen:

    def __init__(self, window_name):
        self.hwnd = None
        self.bitmap = None
        self.save_dc = None
        self.mfc_dc = None
        self.window_name = window_name
        self.screenshot = None

        self.hwnd_dc = None

    def capture_screen(self):
        # Adapted from https://stackoverflow.com/questions/19695214/screenshot-of-inactive-window-printwindow-win32gui
        windll.user32.SetProcessDPIAware()
        self.hwnd = win32gui.FindWindow(None, self.window_name)

        left, top, right, bottom = win32gui.GetClientRect(self.hwnd)
        w = right - left
        h = bottom - top

        self.hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        self.mfc_dc = win32ui.CreateDCFromHandle(self.hwnd_dc)
        self.save_dc = self.mfc_dc.CreateCompatibleDC()
        self.bitmap = win32ui.CreateBitmap()
        self.bitmap.CreateCompatibleBitmap(self.mfc_dc, w, h)
        self.save_dc.SelectObject(self.bitmap)

        windll.user32.PrintWindow(self.hwnd, self.save_dc.GetSafeHdc(), 3)

        bmp_info = self.bitmap.GetInfo()
        bmp_str = self.bitmap.GetBitmapBits(True)

        img = np.frombuffer(bmp_str, dtype=np.uint8).reshape((bmp_info["bmHeight"], bmp_info["bmWidth"], 4))
        img = np.ascontiguousarray(img)[..., :-1]  # make image C_CONTIGUOUS and drop alpha channel

        return img

    def release(self):
        win32gui.DeleteObject(self.bitmap.GetHandle())
        self.save_dc.DeleteDC()
        self.mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwnd_dc)
