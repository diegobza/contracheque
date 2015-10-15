#!/usr/bin/python
# -*- coding: UTF-8 -*-

from escpos import *
import locale
import xml.etree.ElementTree as ET


def p(texto):
    Epson.text(texto.encode('cp860'))


def cpf(cpf):
    return "%s.%s.%s-%s" % (cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])


def real(valor):
    v_float = float(valor)
    v_real = locale.currency(v_float, True, True)
    return v_real


def dict_contra(codigo):
    switcher = {
        199: "VANTAGENS DIVERSAS",
        201: "PREVIDÊNCIA (INSS)",
        202: "PREVIDÊNCIA (REGIME PRÓPRIO)",
        203: "IMPOSTO DE RENDA RETIDO NA FONTE (IRRF)",
        299: "DESCONTOS DIVERSOS"
    }
    return switcher.get(codigo, "nothing")


def p_item(codigo, valor):
    print dict_contra(codigo)
    if codigo >= 201:
        valor = -valor
    print locale.currency(float(valor), False, True)

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

'''Epson = printer.Usb(0x04b8, 0x0e03)
Epson.charcode('portuguese')'''

tree_f = ET.parse('folha.xml')
root = tree_f.getroot()

folha = root.find('folhaPagamento')
contra = folha.find('contracheques')

for i in contra:
    if i.attrib.get('matricula') == '00000001':
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
            valor = j.attrib.get('valor')
            p_item(int(codigo), float(valor))
        '''Epson.cut()'''
