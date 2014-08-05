# -*- coding: utf-8 -*-
# Заголовок "Спецификация"
import xlwt
styletop1 = xlwt.easyxf('font: height 240, name Arial, colour_index brown, bold on, italic off; align: wrap off, vert centre, horiz centre; borders: top 0x00, bottom  0x00, left  0x00, right 0x00;')
#   (номенклатура и объем товаров) приобретаемых товаров - запчасти к бульдозерам  для ПТЭЦ на Р
styletop2 = xlwt.easyxf('font: height 200, name Arial, colour_index brown, bold off, italic on; align: wrap off, vert centre, horiz centre; borders: top 0x00, bottom  0x00, left  0x00, right 0x00;')
#   Заголовки таблиц
styletoptable = xlwt.easyxf('font: height 180, name Arial, colour_index brown, bold on, italic on; align: wrap on, vert centre, horiz centre; borders: top 0x02, bottom  0x02, left  0x02, right 0x02;')
styletoptable2 = xlwt.easyxf('font: height 160, name Arial, colour_index brown, bold off, italic off; align: wrap on, vert centre, horiz centre; borders: top 0x02, bottom  0x02, left  0x02, right 0x02;')
#   Тело таблиц
stylebodytable = xlwt.easyxf('font: height 160, name Arial, colour_index brown, bold off, italic off; align: wrap on, vert centre, horiz left; borders: top 0x01, bottom  0x01, left  0x01, right 0x01;')

#    для групп
stylegroupleft = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour 35; font: height 180, name Arial, colour_index brown, bold on, italic on; align: wrap off, vert centre, horiz left; borders: top 0x02, bottom  0x02, left  0x02, right 0x00;')
stylegroupmiddle = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour 35; font: height 180, name Arial, colour_index brown, bold on, italic on; align: wrap off, vert centre, horiz centre; borders: top 0x02, bottom  0x02, left  0x00, right 0x00;')
stylegroupright = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour 35; font: height 180, name Arial, colour_index brown, bold on, italic on; align: wrap off, vert centre, horiz centre; borders: top 0x02, bottom  0x02, left  0x00, right 0x02;')
#stylegroup.pattern.pattern_fore_colour = 22
#   Подвалы таблицы
stylebottableleft = xlwt.easyxf('font: height 180, name Arial, colour_index brown, bold on, italic on; align: wrap off, vert centre, horiz left; borders: top 0x02, bottom  0x02, left  0x02, right 0x00;')
stylebottablemiddle = xlwt.easyxf('font: height 180, name Arial, colour_index brown, bold on, italic on; align: wrap off, vert centre, horiz centre; borders: top 0x02, bottom  0x02, left  0x00, right 0x00;')
stylebottableright = xlwt.easyxf('font: height 180, name Arial, colour_index brown, bold on, italic on; align: wrap off, vert centre, horiz centre; borders: top 0x02, bottom  0x02, left  0x00, right 0x02;')
#   Подвалы документа
stylebotdoc = xlwt.easyxf('font: height 200, name Arial, colour_index brown, bold off, italic off; align: wrap off, vert centre, horiz left; borders: top 0x00, bottom  0x00, left  0x00, right 0x00;')
#    мелко без обрамления прижать направо
small_no_right = xlwt.easyxf('font: height 160, name Arial, colour_index brown, bold off, italic off; align: wrap off, vert centre, horiz right; borders: top 0x00, bottom  0x00, left  0x00, right 0x00;')
#    Овчинникову
styleofovchin = xlwt.easyxf('font: height 160, name Arial, colour_index brown, bold off, italic off; align: wrap on, vert centre, horiz left; borders: top 0x00, bottom  0x00, left  0x00, right 0x00;')
# Цветной фон средний шрифт обрамленье везде
s1 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour 26; font: height 180, name Arial, colour_index brown, bold on, italic on; align: wrap off, vert centre, horiz left; borders: top 0x02, bottom  0x02, left  0x02, right 0x02;')