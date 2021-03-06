# -*- coding: utf-8 -*-

import os
import serial
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from app.models import Dados, Atuador


def read_serial():
    ser = serial.Serial('/dev/ttyUSB0')

    while True:
        # ler

        dados = ser.readline()

        if len(dados) > 0:
            dados = dados.replace('\r\n', '')
            dados_tipo = dados.split(',')[0]
            if dados_tipo == 'sensor':
                _, umidade_solo, umidade_ar, temperatura = dados.split(',')
                print(float(umidade_solo), float(
                    umidade_ar), float(temperatura))
                save_sensor(float(umidade_solo), float(
                    umidade_ar), float(temperatura))
            else:
                status = dados.split(',')[1]
                print(status)
                save_atuador(status)


def write_serial():
    ser = serial.Serial('/dev/ttyUSB0')

    while True:
        ser.write(b'70;12;1')
        time.sleep(1)



def save_sensor(umidade_solo, umidade_ar, temperatura):
    dados = Dados()
    dados.umidade_solo = umidade_solo
    dados.umidade_ar = umidade_ar
    dados.temperatura = temperatura
    dados.save()


def save_atuador(status):
    atuador = Atuador()
    if status == '1':
        atuador.status = True
    else:
        atuador.status = False

    atuador.save()
    print('Salvou')


def main():
    read_serial()
    # save_data(11,11,11)
    # write_serial()


if __name__ == '__main__':
    main()
