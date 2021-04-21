#!/usr/bin/python
# -*- coding: UTF-8 -*-

import serial
import json
import csv
import struct
# from crccheck.crc import Crc16CcittFalse


gjson = {
    "scanTimes": 11,
    "nameCSV_fine": "fine.csv",
    "nameCSV_average": "average.csv",
    "nameCSV_variance": "variance.csv",
    "nameCSV_baseline": "baseline.csv",
    "nameCSV_touch": "touch.csv",
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
    gjson['baudrate'] = data['save_Touch2csv.py']['baudrate']
    gjson['port'] = data['save_Touch2csv.py']['port']
    gjson['nameCSV_fine'] = data['nameCSV_fine']
    gjson['nameCSV_average'] = data['nameCSV_average']
    gjson['nameCSV_variance'] = data['nameCSV_variance']
    gjson['nameCSV_baseline'] = data['nameCSV_baseline']
    gjson['nameCSV_touch'] = data['nameCSV_touch']
    # print(gjson)


def _save_tsi2tempfile_(filename, data):
    """后面程序的数据交换通过这个文件
    """
    with open(filename, 'w') as f:
        # print('Type:', type(data))
        f.write(str(data))


def _save_fine2csv_(csv_name, data):
    """
    """
    with open(csv_name, 'a') as f:
        f_csv = csv.writer(f)
        for i in range(4*gjson['scanTimes']):
            temp_list = []
            for data_index in range(i, 16*4*gjson['scanTimes'], 4*gjson['scanTimes']):
                temp_list.append(data[data_index])
            f_csv.writerow(temp_list)


def _save_singleData2csv_(csv_name, data):
    """
    """
    with open(csv_name, 'a') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(data)


def save_data2csv():
    """
    """

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
                data_averege.append(struct.unpack('<f', a[1436+i*4:1440+i*4])[0])
            # print('Average:', data_averege)

            # got Variance data
            for i in range(16):
                data_variance.append(struct.unpack('<f', a[1500+i*4:1504+i*4])[0])
            # print('Variance:', data_variance)

            # got Baseline data
            for i in range(16):
                index_baseline = struct.unpack('>B', a[1584:1585])[0]
                if index_baseline == 0:
                    data_baseline.append(struct.unpack('<f', a[1588+i*4:1592+i*4])[0])
                    pass
                elif index_baseline == 1:
                    data_baseline.append(struct.unpack('<f', a[1652+i*4:1656+i*4])[0])
                    pass
                elif index_baseline == 2:
                    data_baseline.append(struct.unpack('<f', a[1716+i*4:1720+i*4])[0])
                else:
                    print('index baseline is wrong...')
                    break
            # print("index baseline: ", index_baseline)
            # print('Baseline:', data_baseline)

            # got Touch valid
            Touch_All = struct.unpack('<H', a[1566:1568])[0]
            for i in range(16):
                if (Touch_All & (2^i)) != 0:
                    data_touch.append(1)
                else:
                    data_touch.append(0)
            # print('Touch:', data_touch)

        else:
            print("data is wrong")
            break

        # save data to csv
        _save_fine2csv_(gjson['nameCSV_fine'], data_fine)
        _save_singleData2csv_(gjson['nameCSV_average'], data_averege)
        _save_singleData2csv_(gjson['nameCSV_variance'], data_variance)
        _save_singleData2csv_(gjson['nameCSV_baseline'], data_baseline)
        _save_singleData2csv_(gjson['nameCSV_touch'], data_touch)
        
    ser.close()


def main():

    readConfiguration()

    '''init csv header'''
    headers = ['ch0', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7',
               'ch8', 'ch9', 'ch10', 'ch11', 'ch12', 'ch13', 'ch14', 'ch15']
    data_filling = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    with open(gjson['nameCSV_fine'], 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
    with open(gjson['nameCSV_average'], 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerow(data_filling)
    with open(gjson['nameCSV_variance'], 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerow(data_filling)
    with open(gjson['nameCSV_baseline'], 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerow(data_filling)
    with open(gjson['nameCSV_touch'], 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerow(data_filling)

    save_data2csv()


if __name__ == "__main__":
    main()
