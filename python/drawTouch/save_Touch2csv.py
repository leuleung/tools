#!/usr/bin/python
# -*- coding: UTF-8 -*-

import serial
import json
from crccheck.crc import Crc16CcittFalse
import csv
import struct


gjson = {
    "scanTimes": 11,
    "nameCSV": "TSI_Fine_All_channle.csv",
    "nameTempfile": "temp",
    "baudrate": 115200,
    "port": "COM0"
}


def readConfiguration(jsonName='TouchConfiguration.json'):
    """通过json配置文件, 获得配置信息.

    """
    global gjson
    f = open(jsonName, 'r')
    data = json.load(f)
    gjson['scanTimes'] = data['scanTimes']
    gjson['nameCSV'] = data['nameCSV']
    gjson['nameTempfile'] = data['nameTempfile']
    gjson['baudrate'] = data['save_TSIFine_csv.py']['baudrate']
    gjson['port'] = data['save_TSIFine_csv.py']['port']
    print(gjson)


def _save_tsi2tempfile_(filename, data):
    """后面程序的数据交换通过这个文件
    """
    with open(filename, 'w') as f:
        # print('Type:', type(data))
        f.write(str(data))


def _save_tsi2csv_(csv_name, data):
    """
    """
    with open(csv_name, 'a') as f:
        f_csv = csv.writer(f)
        for i in range(4*gjson['scanTimes']):
            temp_list = []
            for data_index in range(i, 16*4*gjson['scanTimes'], 4*gjson['scanTimes']):
                temp_list.append(data[data_index])
            f_csv.writerow(temp_list)


def save_data2csv():
    """
    """

    strs = ''

    '''init csv header'''
    headers = ['ch0', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7',
               'ch8', 'ch9', 'ch10', 'ch11', 'ch12', 'ch13', 'ch14', 'ch15']
    with open(gjson['nameCSV'], 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)

    '''init serial'''
    ser = serial.Serial()
    ser.baudrate = gjson['baudrate']
    ser.port = gjson['port']
    ser.stopbits = 2
    ser.open()

    while True:

        data_fine = []
        data_averege = []
        data_variance = []
        data_baseline = []
        data_touch = []

        # got data from uart
        a = ser.read(1848)

        # verify Register
        baseReg = struct.unpack('>I', a[0:4])[0]
        if baseReg == int(3146304):  # Touch Base Register
            
            # got fine data
            index_read = struct.unpack('>B', a[1417:1418])[0]
            if index_read == 0:
                for i in range(704):
                    data_fine.append(struct.unpack('>B', a[7+i:8+i])[0])
            elif index_read == 1:
                for i in range(704):
                    data_fine.append(struct.unpack('>B', a[712+i:713+i])[0])
            else:
                print('index read is wrong...')
                break
            # print('Fine:', data_fine)

            # got average data
            for i in range(16):
                data_averege.append(struct.unpack('>f', a[1436+i*4:1440+i*4])[0])
            # print('Average:', data_averege)

            # got Variance data
            for i in range(16):
                data_variance.append(struct.unpack('>f', a[1500+i*4:1504+i*4])[0])
            # print('Variance:', data_variance)

            # got Baseline data
            for i in range(16):
                index_baseline = struct.unpack('>B', a[1584:1585])[0]
                if index_baseline == 0:
                    data_baseline.append(struct.unpack('>f', a[1588+i*4:1592+i*4])[0])
                    pass
                elif index_baseline == 1:
                    data_baseline.append(struct.unpack('>f', a[1652+i*4:1656+i*4])[0])
                    pass
                elif index_baseline == 2:
                    data_baseline.append(struct.unpack('>f', a[1716+i*4:1720+i*4])[0])
                else:
                    print('index baseline is wrong...')
                    break
            # print("index baseline: ", index_baseline)
            # print('Baseline:', data_baseline)

            # got Touch valid
            Touch_All = struct.unpack('>H', a[1566:1568])[0]
            for i in range(16):
                if (Touch_All & (2^i)) != 0:
                    data_touch.append(1)
                else:
                    data_touch.append(0)
            print('Touch:', data_touch)

        else:
            print("data is wrong")
            break

        # if strs[-1] == '}':
        #     try:
        #         thisJson = json.loads(strs)
        #     except json.decoder.JSONDecodeError:
        #         # 数据传输错误, 有丢包
        #         print('JSON data having Error...')
        #     else:
        #         if thisJson['MessageType'] == 'Log':
        #             print(thisJson['Log'])
        #         elif thisJson['MessageType'] == 'Data':

        #             try:
        #                 '''got data from JSON'''
        #                 data = thisJson['Data']  # data is a int-list
        #             except KeyError:
        #                 print('JSON decode having Error, need retransfer...')
        #             else:
        #                 '''1. 参数校验：CRC16'''
        #                 try:
        #                     if thisJson['Parameter'].find("CRC16") >= 0:
        #                         crc_check = Crc16CcittFalse.calc(data)
        #                         if crc_check == ((thisJson['CRC16'][1]*int(0x100)) + thisJson['CRC16'][0]):
        #                             '''save to csv file'''
        #                             _save_tsi2tempfile_(
        #                                 gjson['nameTempfile'], data)
        #                             _save_tsi2csv_(
        #                                 gjson['nameCSV'], data)
        #                         else:
        #                             print('CRC not Equal, need retransfer...')
        #                     else:
        #                         '''save to csv file'''
        #                         _save_tsi2tempfile_(
        #                             gjson['nameTempfile'], data)
        #                         _save_tsi2csv_(gjson['nameCSV'], data)
        #                 except KeyError:
        #                     print('JSON decode having Error, need retransfer...')
        #     strs = ''
    ser.close()


def main():
    readConfiguration()
    save_data2csv()


if __name__ == "__main__":
    main()
