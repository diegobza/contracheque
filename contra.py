#!/usr/bin/python
# -*- coding: UTF-8 -*-

from escpos import *
import xml.etree.ElementTree as ET


def cpf(cpf):
    return "%s.%s.%s-%s" % (cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])

Epson = printer.Usb(0x04b8, 0x0e03)
Epson.charcode('portuguese')

tree_f = ET.parse('folha.xml')
root = tree_f.getroot()

folha = root.find('folhaPagamento')
contra = folha.find('contracheques')

for i in contra:
    if i.attrib.get('matricula') == '00000002':
        print i.attrib
        Epson.set('center')
        Epson.image('logo-lajes.png')
        Epson.set('center', '', '', '', 2)
        Epson.text('PREFEITURA MUNICIPAL DE LAJES\n')
        Epson.set('left')
        Epson.text('NOME:       ' +
                   i.attrib.get('nome').encode('cp860') + '\n')
        Epson.text('CPF:        ' +
                   cpf(i.attrib.get('cpf')).encode('cp860') + '\n')
        Epson.text('MATRICULA:  ' +
                   i.attrib.get('matricula').encode('cp860') + '\n')
        Epson.cut()
