
import struct
import threading
import serial
import time


class SerialPort:
    def __init__(self, port, buand):
        self.port = serial.Serial(port, buand)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

    def port_open(self):
        if not self.port.isOpen():
            self.port.open()

    def port_close(self):
        self.port.close()

    def send_data(self):
        self.port.write('')

    def read_data(self):
        global is_exit
        global data_bytes
        while not is_exit:
            time.sleep(1)
            count = self.port.inWaiting()
            if count > 0:
                rec_str = self.port.read(count)
                data_bytes = data_bytes + rec_str
                print('当前数据接收总字节数：'+str(len(data_bytes))+' 本次接收字节数：'+str(len(rec_str)))
                # print(data_bytes)
                # print(str(binascii.b2a_hex(rec_str))


serialPort = 'COM4'  # 串口
baudRate = 9600
is_exit = False
data_bytes = bytearray()

if __name__ == '__main__':
    # 打开串口
    mSerial = SerialPort(serialPort, baudRate)
    # 文件写入操作
    out = open('test.txt', 'a+')

    # 开始数据读取
    t1 = threading.Thread(target=mSerial.read_data)
    t1.setDaemon(True)
    t1.start()
    while not is_exit:
        # 对读取的串口数据进行处理
        data_len = len(data_bytes)
        i = 0
        while i < data_len - 1:
            if data_bytes[i] == 0x01 and data_bytes[i + 2] == 0x0C:
                function_code = data_bytes[i + 1]
                if function_code == 0x03:
                    if data_len == 17:  # 判断帧类
                        # struct 解析数据
                        z, y, x = struct.unpack('>fff', data_bytes[i + 3:i + 3 + 12])
                        loc_str = [z, y, x]

                        # 写入csv文件
                        try:
                            with open("test.txt", "a+") as f:
                                loc_str = str(loc_str)
                                f.writelines(loc_str+'/n')
                        except Exception as e:
                            raise e
                i = i + 3 + 12 + 2
            else:
                i = i + 1
        data_bytes[0:i] = b''
