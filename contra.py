#!/usr/bin/python
# -*- coding: UTF-8 -*-

from escpos import *
import xml.etree.ElementTree as ET


def p(texto):
    Epson.text(texto.encode('cp860'))


def cpf(cpf):
    return "%s.%s.%s-%s" % (cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])


def dict_contra(codigo):
    switcher = {
        199: 'Vantagens Diversas'
    }
    return switcher.get(codigo, "nothing")

Epson = printer.Usb(0x04b8, 0x0e03)
Epson.charcode('portuguese')

tree_f = ET.parse('folha.xml')
root = tree_f.getroot()

folha = root.find('folhaPagamento')
contra = folha.find('contracheques')

for i in contra:
    if i.attrib.get('matricula') == '00000002':
        print i.attrib
        '''Epson.set('center')
        Epson.image('logo-lajes.png')
        Epson.set('center', '', '', '', 2)
        p('PREFEITURA MUNICIPAL DE LAJES\n')
        Epson.set('center')
        p('CNPJ: 08.113.466/0001-05\n')
        Epson.set('center', '', 'b')
        p('\nDADOS DO SERVIDOR\n\n')
        Epson.set('left')
        p('NOME:       ' + i.attrib.get('nome') + '\n')
        p('CPF:        ' + cpf(i.attrib.get('cpf')) + '\n')
        p('MATRICULA:  ' + i.attrib.get('matricula') + '\n')'''
        for j in i:
            codigo = j.attrib.get('codigo')
            print codigo
            print dict_contra(codigo)
        '''Epson.cut()'''
