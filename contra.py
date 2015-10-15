#!/usr/bin/python
# -*- coding: UTF-8 -*-

from escpos import *
import locale
import xml.etree.ElementTree as ET


def p(texto):
    Epson.text(texto.encode('cp860'))


def cpf(cpf):
    return "%s.%s.%s-%s" % (cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])


def dict_contra(codigo):
    switcher = {
        199: "VANTAGENS DIVERSAS",
        201: "PREVIDENCIA (INSS)",
        202: "PREVIDENCIA (REGIME PROPRIO)",
        203: "IMPOSTO DE RENDA RETIDO NA FONTE (IRRF)",
        299: "DESCONTOS DIVERSOS"
    }
    return switcher.get(codigo, "nothing")


def p_items(itens):
    total = 0
    for i in itens:
        cod = int(i[0])
        val = float(i[1])

        if cod >= 201:
            val = -val

        total += val

        f_cod = dict_contra(cod)
        f_val = locale.currency(val, False, True)

        espac = 48 - (len(f_cod) + len(f_val))
        print espac

        if espac > 0:
            Epson.set('left')
            p(f_cod + espac * ' ' + f_val + '\n')

    Epson.set('right')
    p('-------\n')
    Epson.set('right', '', 'b')
    f_total = locale.currency(total, True, True)
    p('TOTAL  ' + f_total + '\n')


def intro():
    Epson.set('center')
    Epson.image('logo-lajes.png')
    Epson.set('center', '', '', '', 2)
    p('PREFEITURA MUNICIPAL DE LAJES\n')
    Epson.set('center')
    p('CNPJ: 08.113.466/0001-05\n')
    Epson.set('center', '', 'b')
    p('\nDADOS DO SERVIDOR\n\n')


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

Epson = printer.Usb(0x04b8, 0x0e03)
Epson.charcode('portuguese')

tree_f = ET.parse('folha.xml')
root = tree_f.getroot()

folha = root.find('folhaPagamento')
contra = folha.find('contracheques')

for i in contra:
    if i.attrib.get('matricula') == '00000001':
        intro()
        Epson.set('left')
        p('NOME:       ' + i.attrib.get('nome') + '\n')
        p('CPF:        ' + cpf(i.attrib.get('cpf')) + '\n')
        p('MATRICULA:  ' + i.attrib.get('matricula') + '\n')
        Epson.set('center', '', 'b')
        p('\nCONTRACHEQUE\n\n')
        itens = []
        for j in i:
            item = [j.attrib.get('codigo'), j.attrib.get('valor')]
            itens.append(item)
        p_items(itens)
        Epson.cut()
