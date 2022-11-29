import cv2
from pyzbar import pyzbar
import playsound


class BarcodeReader:
    def __init__(self):
        self.camera = cv2.VideoCapture(1)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def read(self):
        _, frame = self.camera.read()
        cv2.imshow('Barcode Reader', frame)
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            colour = (255, 0, 0)
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, colour, 1)
            playsound.playsound('beep.mp3', True)
            return barcode_info
        return None

    def __del__(self):
        self.camera.release()


class IPWebcamBarcodeReader:
    def __init__(self, ip):
        self.ip = ip
        self.camera = cv2.VideoCapture(f'http://{ip}/video')

    def read(self):
        _, frame = self.camera.read()
        cv2.imshow('Barcode Reader', frame)
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            colour = (255, 0, 0)
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, colour, 1)
            playsound.playsound('beep.mp3', True)
            return barcode_info
        return None

    def __del__(self):
        self.camera.release()


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        frame_flip = cv2.flip(frame, 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            colour = (255, 0, 0)
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, colour, 1)
            playsound.playsound('dashboard/beep.mp3', True)
            return barcode_info
        return jpeg.tobytes()


if __name__ == "__main__":
    reader = BarcodeReader()
    while True:
        barcode = reader.read()
        if barcode:
            print(barcode)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break