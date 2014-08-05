# -*- coding: utf-8 -*-
import xlwt
import sys
from datetime import date
from django.db.models import Max,Min
import styles
from supplier.ren import models
from django.http import HttpResponseRedirect
from models import register,factory
from views import clearborder,list2excel,bottablespec2excel,setwidth #,bodyspec2excelR,bodyspec2excelE,
##############################################################################################
#              Класс Спецификации по запланированной работе по эксплуатации  (id-touse.id)   #
##############################################################################################
class Tspeca_of_work():
#    filename = u'/home/plaksa/supplier/media/'+self.root.name.replace('/','_').replace(" ","_")+u'_Эксплуатация.xls'
    filename = u'%s_Эксплуатация.xls'
    def __init__(self,request,id):
#        self.filename = 'speca_of_exp.xls'
        self.root = models.touse.objects.get(pk = id)
        self.path_local = u'/home/plaksa/supplier/media/'
        self.path_web = u'http://172.27.80.127/supplier/media/'+self.__class__.filename % self.root.name.replace('/','_').replace(" ","_")
        self.numpp = 1
        self.countcol = 7
        self.width_of_cols = [1200,10000,3000,3000,3000,5000,5000,5000]
        self.col2a = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.curr_row = 2
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet('Sheet1')
        self.clear_border()
        self.set_width()
        self.headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Кол-во',u'Цена',u'Сумма',]
        self.write_top()
        self.recursion(self.root)
#        self.book.save(u'/home/plaksa/supplier/media/'+self.root.name.replace('/','_').replace(" ","_")+u'_Эксплуатация.xls')
        sss = self.path_local+self.__class__.filename % self.root.name.replace('/','_').replace(" ","_")
        self.book.save(sss.encode('utf-8'))

##############################################################################################
#                             Запись шапки таблицы                                           #
##############################################################################################
    def write_top(self):
        self.sheet.row(self.curr_row).height = 500
        for col in range(0,len(self.headers)):
            self.sheet.write(self.curr_row,col,self.headers[col],styles.styletoptable,)
        self.curr_row += 1
##############################################################################################
#                             Процедура очистки обрамления колонок                           #
##############################################################################################
    def clear_border(self):
        for col in range(0,self.countcol-1):
            self.sheet.write(0,col,'',styles.styletop1)
        self.curr_row += 1
##############################################################################################
#                Процедура установки ширины колонок                                          #
##############################################################################################
    def set_width(self):
        for numcol in range(0,len(self.width_of_cols)):
            self.sheet.col(numcol).width = self.width_of_cols[numcol]

############################################################################
#            Рекурсивная процедура обхода tree_view дерева                 #
############################################################################
    def recursion(self,parent):
        if parent == None:
            return
        self.sheet.write(self.curr_row,1,parent.name,styles.s1,)
        self.curr_row += 1
        for reg in models.register.objects.filter(touse = parent).filter(ison = True):
            self.sheet.write(self.curr_row,0,self.numpp,styles.stylebodytable,)
            self.sheet.write(self.curr_row,1,reg.materials.name,styles.stylebodytable,)
            self.sheet.write(self.curr_row,2,reg.materials.units.name,styles.stylebodytable,)
            self.sheet.write(self.curr_row,3,reg.working,styles.stylebodytable,)
            self.sheet.write(self.curr_row,4,reg.materials.price,styles.stylebodytable,)
            self.sheet.write(self.curr_row,5,reg.sumworking,styles.stylebodytable,)
            self.curr_row += 1
            self.numpp += 1
        query = parent.get_children().filter(ison = True)
        for child in query:
            self.recursion(child)

##############################################################################################
#              Класс Спецификации по запланированной работе по ремонту       (id-touse.id)   #
##############################################################################################
class Tspeca_of_repair(Tspeca_of_work):
    filename = u'%s_Ремонт.xls'
#    filename = u'/home/plaksa/supplier/media/'+self.root.name.replace('/','_').replace(" ","_")+u'_Ремонт.xls'
############################################################################
#            Рекурсивная процедура обхода tree_view дерева                 #
############################################################################
    def recursion(self,parent):
        if parent == None:
            return
        self.sheet.write(self.curr_row,1,parent.name,styles.s1,)
        self.curr_row += 1
        for reg in models.register.objects.filter(touse = parent).filter(ison = True):
            self.sheet.write(self.curr_row,0,self.numpp,styles.stylebodytable,)
            self.sheet.write(self.curr_row,1,reg.materials.name,styles.stylebodytable,)
            self.sheet.write(self.curr_row,2,reg.materials.units.name,styles.stylebodytable,)
            self.sheet.write(self.curr_row,3,reg.repair,styles.stylebodytable,)
            self.sheet.write(self.curr_row,4,reg.materials.price,styles.stylebodytable,)
            self.sheet.write(self.curr_row,5,reg.sumrepair,styles.stylebodytable,)
            self.curr_row += 1
            self.numpp += 1
        query = parent.get_children().filter(ison = True)
        for child in query:
            self.recursion(child)

def speca_of_work(request,id):
#    one = Tspeca_of_work(request,id) группировка по планируемым работам не удалять
    one = Tspeca_of_work_kind(request,id)
    return HttpResponseRedirect(one.path_web)


def speca_of_repair(request,id):
    one = Tspeca_of_repair_kind(request,id)
    return HttpResponseRedirect(one.path_web)


##############################################################################################
#                             Процедура формирования техзадания по главным категориям        #
##############################################################################################
#from xlwt import *
import xlwt
import sys
from datetime import date
from django.db.models import Max,Min
from django.db.models import Sum
def tz_by_high(request):
    colall = 8
    sd = 0 # shiftdown
    sr = 0 # shiftright
    specwidth = [1200,10000,3000,3000,3000,5000,5000,5000]
    tzwidth = [4000,12000,5500,4500,5000,3000,3500,7000,5500]
# Заголовок "Спецификация"
    styletop1 = xlwt.easyxf('font: height 240, name Arial, colour_index brown, bold on, italic off; align: wrap off, vert centre, horiz centre; borders: top 0x00, bottom  0x00, left  0x00, right 0x00;')
#   (номенклатура и объем товаров) приобретаемых товаров - запчасти к бульдозерам  для ПТЭЦ на Р
    styletop2 = xlwt.easyxf('font: height 200, name Arial, colour_index brown, bold off, italic on; align: wrap off, vert centre, horiz centre; borders: top 0x00, bottom  0x00, left  0x00, right 0x00;')
#   Заголовки таблиц
    styletoptable = xlwt.easyxf('font: height 180, name Arial, colour_index brown, bold on, italic on; align: wrap on, vert centre, horiz centre; borders: top 0x02, bottom  0x02, left  0x02, right 0x02;')
    styletoptable2 = xlwt.easyxf('font: height 160, name Arial, colour_index brown, bold off, italic off; align: wrap on, vert centre, horiz centre; borders: top 0x02, bottom  0x02, left  0x02, right 0x02;')
#   Тело таблиц
    stylebodytable = xlwt.easyxf('font: height 160, name Arial, colour_index brown, bold off, italic off; align: wrap on, vert centre, horiz left; borders: top 0x01, bottom  0x01, left  0x01, right 0x01;')
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

    topspec = list()
    topspec.append([0,4,u'Спецификация',styletop1])
    topspec.append([1,4,u'topspec[1][2]',styletop2])
    topspec.append([3,0,u'№ пп',styletoptable,2200])
    topspec.append([3,1,u'Номенклатура приобретаемого товара',styletoptable])
    topspec.append([3,2,u'Единицы измерения',styletoptable])
    topspec.append([3,3,u'Количество',styletoptable])
    topspec.append([3,4,u'Планируемая стоимость,  руб.    (с учетом транспортных расходов, без учета НДС) ',styletoptable])
    topspec.append([3,5,u'Требования к продукции (указыается требоваания ГОСТ, ТУ, № чертежей или иная существенная информация, четко идентифицирующая предмет закупки)',styletoptable])
    topspec.append([3,6,u'Информация о приемленности аналогов (указать информацию о возможности применения аналогов заменителей ) Приемлемы/неприемлемы',styletoptable])
    topspec.append([3,7,u'Примечание (указывается иная значимая и существенная информация в рамках данной закупки, например обязательное наличие сертификата)',styletoptable])
    topspec.append([4,0,u'1',styletoptable2,300])
    topspec.append([4,1,u'2',styletoptable2])
    topspec.append([4,2,u'3',styletoptable2])
    topspec.append([4,3,u'4',styletoptable2])
    topspec.append([4,4,u'5',styletoptable2])
    topspec.append([4,5,u'6',styletoptable2])
    topspec.append([4,6,u'7',styletoptable2])
    topspec.append([4,7,u'8',styletoptable2])
# опции
    opt = models.mo.objects.get()
    botspec = []
    botspec.append([6,1,opt.bossstate,stylebotdoc])
    botspec.append([6,6,opt.bossfio,stylebotdoc])
    botspec.append([7,6,u'(ФИО)',stylebotdoc])
    botspec.append([9,1,opt.repairstate,stylebotdoc])
    botspec.append([9,6,opt.repairfio,stylebotdoc])
    botspec.append([10,6,u'(ФИО)',stylebotdoc])
    botspec.append([12,1,opt.omtsstate,stylebotdoc])
    botspec.append([12,6,opt.omtsfio,stylebotdoc])
    botspec.append([13,6,u'(ФИО)',stylebotdoc])
    botspec.append([15,1,u'Исполнитель (ФИО, тел., факс, электронный адрес):',stylebotdoc])
    botspec.append([15,6,u'Овчинников Сергей Анатольевич, мастер ОМТС Читинской Генерации , филиала ОАО "ТГК-14"   (3022) 38-72-30, факс (3022) 38-72-23, kandaurov@tgk-14.com',styleofovchin,2200])

    toptz = []
    toptz.append([0,8,u'Приложение 3',small_no_right])
    toptz.append([1,8,u'к приказу №______     от ____________',small_no_right])
    toptz.append([3,8,u'Начальнику ОТЗД ОАО "ТГК-14"',small_no_right])
    toptz.append([6,3,u'Техническое задание на проведение конкурентных закупочных процедур',styletop1])
    toptz.append([7,3,u'(закупка ТМЦ и МТР)',styletop2])
    toptz.append([9,0,u'Наименование структурного подразделения (предприяти)-потребителя продукции.',styletoptable,2200])
    toptz.append([9,1,u'Наименование закупки (указыается согласно ГКПЗ или решению ЦЗК, в случае если закупка не является плановой)',styletoptable])
    toptz.append([9,2,u'Идентификатор по ГКПЗ (указыается в формате - ГКПЗ 200___ год, Раздел №___, МТР и ТМЦ, закупка № ____, лот №___, в случае отсутствия в ГКПЗ указывать - "неплановая, Раздел №___, МТР и ТМЦ")',styletoptable])
    toptz.append([9,3,u'Планируемая цена (стоимость) лота ,  руб.    (с учетом транспортных расходов, без учета НДС)',styletoptable])
    toptz.append([9,4,u'Место поставки, реквизиты грузополучателя',styletoptable])
    toptz.append([9,5,u'Срок поставки продукции',styletoptable])
    toptz.append([9,6,u'Вид оплаты * (указывается наихудший вид оплаты, но приемлемый для покупателя)',styletoptable])
    toptz.append([9,7,u'Контактное лицо для обращений потенциальных участников процедуры с целью уточнения возможных вопросов (указывается полностью фамилия, имя, отчество, должность, телефон, факс, электронный адрес)',styletoptable])
    toptz.append([9,8,u'Примечание (указывается ссылка на решение ЦЗК в случае отсутствия в (плане) ГКПЗ, а также иная значимая и существенная информация в рамках данной закупки)',styletoptable])
    toptz.append([10,0,u'1',styletoptable2,300])
    toptz.append([10,1,u'2',styletoptable2])
    toptz.append([10,2,u'3',styletoptable2])
    toptz.append([10,3,u'4',styletoptable2])
    toptz.append([10,4,u'5',styletoptable2])
    toptz.append([10,5,u'6',styletoptable2])
    toptz.append([10,6,u'7',styletoptable2])
    toptz.append([10,7,u'8',styletoptable2])
    toptz.append([10,8,u'9',styletoptable2])

    bottz = []
    bottz.append([16,1,opt.bossstate,stylebotdoc])
    bottz.append([16,6,opt.bossfio,stylebotdoc])
    bottz.append([17,6,u'(ФИО)',stylebotdoc])
    bottz.append([9,1,opt.repairstate,stylebotdoc])
    bottz.append([9,6,opt.repairfio,stylebotdoc])
    bottz.append([10,6,u'(ФИО)',stylebotdoc])
    bottz.append([12,1,opt.omtsstate,stylebotdoc])
    bottz.append([12,6,opt.omtsfio,stylebotdoc])
    bottz.append([13,6,u'(ФИО)',stylebotdoc])
    bottz.append([15,1,u'Исполнитель (ФИО, тел., факс, электронный адрес):',stylebotdoc])
    bottz.append([15,6,u'Овчинников Сергей Анатольевич, мастер ОМТС Читинской Генерации , филиала ОАО "ТГК-14"   (3022) 38-72-30, факс (3022) 38-72-23, kandaurov@tgk-14.com',styleofovchin,2200])

###########################################################################################################
#                                           Ремонт                                                        #
###########################################################################################################

    for hikind in models.hikind.objects.all():
        data = register.objects.filter(materials__kind__hikind__id = hikind.id).aggregate(Sum('repair'))
        bottz[10] = [15,6,hikind.curator.name+', '+hikind.curator.post+u',телефон - '+hikind.curator.phonecity+u', факс - '+ hikind.curator.phonefax+', '+hikind.curator.email,styleofovchin,2200]
        if not (data) :
            continue
        if data['repair__sum']>0:
            wbook = xlwt.Workbook()
            sumofgroup = 0
            sg = 0
            for tec in factory.objects.all():
                data = register.objects.filter(materials__kind__hikind__id = hikind.id,cex__factory__id = tec.id).aggregate(Sum('repair'))
                if not (data):
                    continue
                if data['repair__sum']<=0:
                    continue
                row = 1
                sheet = wbook.add_sheet(u'Спецификация по '+tec.name)
#            очистка обрамления основного листа
                clearborder(8,sheet,styletop1)
                row += 1
#            шапка спецификации
                topspec[1][2] = u'(номенклатура и объем товаров) приобретаемых товаров - '+tec.name+u' Ремонт'
                row = list2excel(row,topspec,sheet)
#            Тело спецификации
                sg,row = bodyspec2excelR(hikind,row,tec,sheet,stylebodytable)
                sumofgroup = sg + sumofgroup
#            Подвал таблицы спецификации
                bottablespec2excel(colall,row,sheet,sg,stylebottableleft,stylebottablemiddle,stylebottableright)
#            Подвал спецификации
                botspec[10] = [15,6,hikind.curator.name+', '+hikind.curator.post+u',телефон - '+hikind.curator.phonecity+u', факс - '+ hikind.curator.phonefax+', '+hikind.curator.email,styleofovchin,2200]
                row = list2excel(row,botspec,sheet)
#            Ширина колонок
                setwidth(specwidth,sheet)
            sheet = wbook.add_sheet(u'ТЗ')
#            Ширина колонок
            setwidth(tzwidth,sheet)
#             Шапка техзадания
            row = 1
            row = list2excel(row,toptz,sheet)
#             тело техзадания
#                график поставки
            data = register.objects.filter(materials__kind__hikind__id = hikind.id).aggregate(Min('datesupply'),Max('datesupply'))
            sheet.row(row).height = 3000
            sheet.write(row,0,opt.name,stylebodytable,)
            sheet.write(row,1,hikind.name,stylebodytable,)
            sheet.write(row,2,u'ГКПЗ 200_13_ год, Раздел №__, МТР и ТМЦ, закупка, лот ',stylebodytable,)
            sheet.write(row,3,sumofgroup,stylebodytable,)
            sheet.write(row,4,opt.name+', '+opt.realaddr+', '+opt.lawaddr+u', код грузополучателя - '+opt.codesource+u', ОКПО - '+opt.okpo+u', ИНН - '+opt.inn+u', КПП - '+opt.kpp,stylebodytable,)
            sheet.write(row,5,str(data['datesupply__min'].date())+u'-'+str(data['datesupply__max'].date()),stylebodytable,)
            sheet.write(row,6,u'оплата по факту поставки',stylebodytable,)
            sheet.write(row,7,hikind.curator.name+' '+hikind.curator.post+ u' телефон:'+hikind.curator.phonecity+u' факс:'+hikind.curator.phonefax+u' эл.почта:'+hikind.curator.email,stylebodytable,)
            sheet.write(row,8,u'Значение поля пока незаполнено',stylebodytable,)
#             подвал техзадания
            row = row + 1
            row = list2excel(row,bottz,sheet)
            sss = u'/home/plaksa/supplier/media/'+hikind.name.replace('/','_').replace(" ","_")+u'_Рем.xls'
            wbook.save(sss.encode('utf-8'))

###########################################################################################################
#                                           Эксплуатация                                                  #
###########################################################################################################
    bottz[3][2] = opt.workstate
    bottz[4][2] = opt.workfio
    botspec[3][2] = opt.workstate
    botspec[4][2] = opt.workfio
    for hikind in models.hikind.objects.all():
        data = register.objects.filter(materials__kind__hikind__id = hikind.id).aggregate(Sum('working'))
        bottz[10] = [15,6,hikind.curator.name+', '+hikind.curator.post+u',телефон - '+hikind.curator.phonecity+u', факс - '+ hikind.curator.phonefax+', '+hikind.curator.email,styleofovchin,2200]
        if not (data) :
            continue
        if data['working__sum']>0:
            wbook = xlwt.Workbook()
            sumofgroup = 0
            sg = 0
            for tec in factory.objects.all():
                data = register.objects.filter(materials__kind__hikind__id = hikind.id,cex__factory__id = tec.id).aggregate(Sum('working'))
                if not (data):
                    continue
                if data['working__sum']<=0:
                    continue
                row = 1
                sheet = wbook.add_sheet(u'Спецификация по '+tec.name)
#            очистка обрамления
                clearborder(8,sheet,styletop1)
                row += 1
#            шапка спецификации
                topspec[1][2] = u'(номенклатура и объем товаров) приобретаемых товаров - '+tec.name+u' Эксплуатация'
                row = list2excel(row,topspec,sheet)
#            Тело спецификации
                sg,row = bodyspec2excelE(hikind,row,tec,sheet,stylebodytable)
                sumofgroup = sg + sumofgroup
#            Подвал таблицы спецификации
                bottablespec2excel(colall,row,sheet,sg,stylebottableleft,stylebottablemiddle,stylebottableright)
#            Подвал спецификации
                row = list2excel(row,botspec,sheet)
#            Ширина колонок
                setwidth(specwidth,sheet)
            sheet = wbook.add_sheet(u'ТЗ')
#            Ширина колонок
            setwidth(tzwidth,sheet)
#             Шапка техзадания
            row = 1
            row = list2excel(row,toptz,sheet)
#             тело техзадания
            sheet.row(row).height = 3000
            sheet.write(row,0,opt.name,stylebodytable,)
            sheet.write(row,1,hikind.name,stylebodytable,)
            sheet.write(row,2,u'ГКПЗ 200_13_ год, Раздел №__, МТР и ТМЦ, закупка, лот ',stylebodytable,)
            sheet.write(row,3,sumofgroup,stylebodytable,)
            sheet.write(row,4,opt.name+', '+opt.realaddr+', '+opt.lawaddr+u', код грузополучателя - '+opt.codesource+u', ОКПО - '+opt.okpo+u', ИНН - '+opt.inn+u', КПП - '+opt.kpp,stylebodytable,)
            data = register.objects.filter(materials__kind__hikind__id = hikind.id).aggregate(Min('datesupply'),Max('datesupply'))
            sheet.write(row,5,str(data['datesupply__min'].date())+u'-'+str(data['datesupply__max'].date()),stylebodytable,)
            sheet.write(row,6,u'оплата по факту поставки',stylebodytable,)
            sheet.write(row,7,hikind.curator.name+' '+hikind.curator.post+ u' телефон:'+hikind.curator.phonecity+u' факс:'+hikind.curator.phonefax+u' эл.почта:'+hikind.curator.email,stylebodytable,)
            sheet.write(row,8,u'Что характерно?',stylebodytable,)
#             подвал техзадания
            row = row + 1
            row = list2excel(row,bottz,sheet)
            sss = '/home/plaksa/supplier/media/'+hikind.name.replace('/','_').replace(" ","_")+u'_Экс.xls'
            wbook.save(sss.encode('utf-8'))
    return HttpResponseRedirect('/supplier/')

##############################################################################################
#                             Процедура выгрузки в эксель тела спецификации РЕМОНТ           #
##############################################################################################
def bodyspec2excelR(hikind,row,tec,sheet,stylebodytable):
    numpp = 1
    sumofgroup = 0
    listofdate = []
    for material in models.materials.objects.filter(kind__hikind__id = hikind.id):
        data = register.objects.filter(materials = material,cex__factory__id = tec.id).aggregate(Sum('repair'))
        if (data['repair__sum'] == None) or (data['repair__sum'] == 0):
            continue
#                Номер по порядку
        sheet.write(row,0,str(numpp),stylebodytable,)
#                Наименование
        sheet.write(row,1,material.name,stylebodytable,)
#                Единицы измерения
        sheet.write(row,2,material.units.name,stylebodytable,)
#                Количество
        sheet.write(row,3,data['repair__sum'],stylebodytable,)
#                Цена
        sheet.write(row,4,material.price/1000,stylebodytable,)
        sumofgroup = sumofgroup + data['repair__sum']*material.price/1000
#                Требования 
        sheet.write(row,5,material.requirement,stylebodytable,)
#                Аналоги
        sheet.write(row,6,material.allowchange,stylebodytable,)
#                Примечание
        sheet.write(row,7,material.extrainfo,stylebodytable,)
        sheet.row(row).height = 500
        row += 1
        numpp += 1
    return sumofgroup,row
##############################################################################################
#                             Процедура выгрузки в эксель тела спецификации ЭКСПЛУАТАЦИЯ     #
##############################################################################################
def bodyspec2excelE(hikind,row,tec,sheet,stylebodytable):
    numpp = 1
    sumofgroup = 0
    for material in models.materials.objects.filter(kind__hikind__id = hikind.id):
        data = register.objects.filter(materials = material,cex__factory__id = tec.id).aggregate(Sum('working'))
        if (data['working__sum'] == None) or (data['working__sum'] == 0):
            continue
#                Номер по порядку
        sheet.write(row,0,str(numpp),stylebodytable,)
#                Наименование
        sheet.write(row,1,material.name,stylebodytable,)
#                Единицы измерения
        sheet.write(row,2,material.units.name,stylebodytable,)
#                Количество
        sheet.write(row,3,data['working__sum'],stylebodytable,)
#                Цена
        sheet.write(row,4,material.price/1000,stylebodytable,)
        sumofgroup = sumofgroup + data['working__sum']*material.price/1000
#                Требования 
        sheet.write(row,5,material.requirement,stylebodytable,)
#                Аналоги
        sheet.write(row,6,material.allowchange,stylebodytable,)
#                Примечание
        sheet.write(row,7,material.extrainfo,stylebodytable,)
        sheet.row(row).height = 500
        row += 1
        numpp += 1
    return sumofgroup,row




########################################################################################################################
#              Класс Спецификации по запланированной работе по ремонту       группировка по категориям (id-touse.id)   #
########################################################################################################################
class Tspeca_of_repair_kind():
#    filename = u'/home/plaksa/supplier/media/'+self.root.name.replace('/','_').replace(" ","_")+u'_Эксплуатация.xls'
    filename = u'%s_Ремонт.xls'
    def __init__(self,request,id):
#        self.filename = 'speca_of_exp.xls'
        self.itogswork = []
        self.itogskind = []
        self.root = models.touse.objects.get(pk = id)
        self.path_local = u'/home/plaksa/supplier/media/'
        self.path_web = u'http://172.27.80.127/supplier/media/'+self.__class__.filename % self.root.name.replace('/','_').replace(" ","_")
        self.numpp = 1
        self.countcol = 7
        self.width_of_cols = [1200,10000,3000,3000,3000,5000,5000,5000]
        self.col2a = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.curr_row = 2
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet('Sheet1')
        self.clear_border()
        self.set_width()
        self.headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Кол-во',u'Цена',u'Сумма',]
        self.write_top()
        self.body(self.root)
#        self.book.save(u'/home/plaksa/supplier/media/'+self.root.name.replace('/','_').replace(" ","_")+u'_Эксплуатация.xls')
        self.sheet.write(self.curr_row,1,u'Итого по отчету ',styles.stylebodytable,)
        list_cells = ''
        for one in self.itogswork:
            list_cells = list_cells +'+'+self.col2a[5]+str(one+1)
        if len(list_cells)>0:
            self.sheet.write(self.curr_row,5,xlwt.Formula(list_cells[1:]),styles.stylebodytable,)
        sss = self.path_local+self.__class__.filename % self.root.name.replace('/','_').replace(" ","_")
        self.book.save(sss.encode('utf-8'))
        self.book = None
##############################################################################################
#                             Запись шапки таблицы                                           #
##############################################################################################
    def write_top(self):
        self.sheet.row(self.curr_row).height = 500
        for col in range(0,len(self.headers)):
            self.sheet.write(self.curr_row,col,self.headers[col],styles.styletoptable,)
        self.curr_row += 1
##############################################################################################
#                             Процедура очистки обрамления колонок                           #
##############################################################################################
    def clear_border(self):
        for col in range(0,self.countcol-1):
            self.sheet.write(0,col,'',styles.styletop1)
        self.curr_row += 1
##############################################################################################
#                Процедура установки ширины колонок                                          #
##############################################################################################
    def set_width(self):
        for numcol in range(0,len(self.width_of_cols)):
            self.sheet.col(numcol).width = self.width_of_cols[numcol]

############################################################################
#            Рекурсивная процедура обхода tree_view дерева                 #
############################################################################
    def body(self,parent):
        if parent == None:
            return
        self.sheet.write(self.curr_row,1,u'Планируемая работа '+parent.name,styles.s1,)
        self.curr_row += 1
        for kind in models.kind.objects.all().order_by('name'):
            data = models.register.objects.filter(touse = parent,ison = True,materials__kind__id=kind.id).aggregate(Sum('repair'))
            if (data['repair__sum'] == None) or (data['repair__sum'] == 0):
                continue
#            if models.register.objects.filter(touse = parent,ison = True,materials__kind__id=kind.id).count()>0:
            self.sheet.write(self.curr_row,1,u'Категория '+kind.name,styles.s1,)
            self.curr_row += 1
            self.itogskind.append({'rowbeg':self.curr_row,'rowend':-1})
            for reg in models.register.objects.filter(touse = parent,ison = True,materials__kind__id=kind.id):
                self.sheet.write(self.curr_row,0,self.numpp,styles.stylebodytable,)
                self.sheet.write(self.curr_row,1,reg.materials.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,2,reg.materials.units.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,3,reg.repair,styles.stylebodytable,)
                self.sheet.write(self.curr_row,4,reg.materials.price,styles.stylebodytable,)
                self.sheet.write(self.curr_row,5,reg.sumrepair,styles.stylebodytable,)
                self.curr_row += 1
                self.numpp += 1
            self.itogskind[-1]['rowend']=self.curr_row
            self.sheet.write(self.curr_row,1,u'Итого по категории '+kind.name,styles.stylebodytable,)
            self.sheet.write(self.curr_row,5,xlwt.Formula(u'SUM('+self.col2a[5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                     u':'+self.col2a[5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
            self.curr_row += 1
        self.sheet.write(self.curr_row,1,u'Итого по планируемой работе '+parent.name,styles.stylebodytable,)
        list_cells = ''
        for one in self.itogskind:
            list_cells = list_cells + '+'+self.col2a[5]+str(one['rowend']+1)
        if len(list_cells)>0:
            self.sheet.write(self.curr_row,5,xlwt.Formula(list_cells[1:]),styles.stylebodytable,)
        self.itogswork.append(self.curr_row)
        self.curr_row += 1
        query = parent.get_children().filter(ison = True)
        for child in query:
            self.body(child)

########################################################################################################################
#              Класс Спецификации по запланированной работе по эксплуатаци   группировка по категориям (id-touse.id)   #
########################################################################################################################
class Tspeca_of_work_kind():
#    filename = u'/home/plaksa/supplier/media/'+self.root.name.replace('/','_').replace(" ","_")+u'_Эксплуатация.xls'
    filename = u'%s_Эксплуатация.xls'
    def __init__(self,request,id):
#        self.filename = 'speca_of_exp.xls'
        self.itogswork = []
        self.itogskind = []
        self.root = models.touse.objects.get(pk = id)
        self.path_local = u'/home/plaksa/supplier/media/'
        self.path_web = u'http://172.27.80.127/supplier/media/'+self.__class__.filename % self.root.name.replace('/','_').replace(" ","_")
        self.numpp = 1
        self.countcol = 7
        self.width_of_cols = [1200,10000,3000,3000,3000,5000,5000,5000]
        self.col2a = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.curr_row = 2
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet('Sheet1')
        self.clear_border()
        self.set_width()
        self.headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Кол-во',u'Цена',u'Сумма',]
        self.write_top()
        self.body(self.root)
#        self.book.save(u'/home/plaksa/supplier/media/'+self.root.name.replace('/','_').replace(" ","_")+u'_Эксплуатация.xls')
        self.sheet.write(self.curr_row,1,u'Итого по отчету ',styles.stylebodytable,)
        list_cells = ''
        for one in self.itogswork:
            list_cells = list_cells +'+'+self.col2a[5]+str(one+1)
        if len(list_cells)>0:
            self.sheet.write(self.curr_row,5,xlwt.Formula(list_cells[1:]),styles.stylebodytable,)
        sss = self.path_local+self.__class__.filename % self.root.name.replace('/','_').replace(" ","_")
#        self.book.save(self.path_local+self.__class__.filename % self.root.name.replace('/','_').replace(" ","_"))
        self.book.save(sss.encode('utf-8'))
        self.book = None
##############################################################################################
#                             Запись шапки таблицы                                           #
##############################################################################################
    def write_top(self):
        self.sheet.row(self.curr_row).height = 500
        for col in range(0,len(self.headers)):
            self.sheet.write(self.curr_row,col,self.headers[col],styles.styletoptable,)
        self.curr_row += 1
##############################################################################################
#                             Процедура очистки обрамления колонок                           #
##############################################################################################
    def clear_border(self):
        for col in range(0,self.countcol-1):
            self.sheet.write(0,col,'',styles.styletop1)
        self.curr_row += 1
##############################################################################################
#                Процедура установки ширины колонок                                          #
##############################################################################################
    def set_width(self):
        for numcol in range(0,len(self.width_of_cols)):
            self.sheet.col(numcol).width = self.width_of_cols[numcol]

############################################################################
#            Рекурсивная процедура обхода tree_view дерева                 #
############################################################################
    def body(self,parent):
        if parent == None:
            return
        self.sheet.write(self.curr_row,1,u'Планируемая работа '+parent.name,styles.s1,)
        self.curr_row += 1
        for kind in models.kind.objects.all().order_by('name'):
            data = models.register.objects.filter(touse = parent,ison = True,materials__kind__id=kind.id).aggregate(Sum('working'))
            if (data['working__sum'] == None) or (data['working__sum'] == 0):
                continue
#            if models.register.objects.filter(touse = parent,ison = True,materials__kind__id=kind.id).count()>0:
            self.sheet.write(self.curr_row,1,u'Категория '+kind.name,styles.s1,)
            self.curr_row += 1
            self.itogskind.append({'rowbeg':self.curr_row,'rowend':-1})
            for reg in models.register.objects.filter(touse = parent,ison = True,materials__kind__id=kind.id):
                self.sheet.write(self.curr_row,0,self.numpp,styles.stylebodytable,)
                self.sheet.write(self.curr_row,1,reg.materials.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,2,reg.materials.units.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,3,reg.working,styles.stylebodytable,)
                self.sheet.write(self.curr_row,4,reg.materials.price,styles.stylebodytable,)
                self.sheet.write(self.curr_row,5,reg.sumworking,styles.stylebodytable,)
                self.curr_row += 1
                self.numpp += 1
            self.itogskind[-1]['rowend']=self.curr_row
            self.sheet.write(self.curr_row,1,u'Итого по категории '+kind.name,styles.stylebodytable,)
            self.sheet.write(self.curr_row,5,xlwt.Formula(u'SUM('+self.col2a[5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                     u':'+self.col2a[5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
            self.curr_row += 1
        self.sheet.write(self.curr_row,1,u'Итого по планируемой работе '+parent.name,styles.stylebodytable,)
        list_cells = ''
        for one in self.itogskind:
            list_cells = list_cells + '+'+self.col2a[5]+str(one['rowend']+1)
        if len(list_cells)>0:
            self.sheet.write(self.curr_row,5,xlwt.Formula(list_cells[1:]),styles.stylebodytable,)
        self.itogswork.append(self.curr_row)
        self.curr_row += 1
        query = parent.get_children().filter(ison = True)
        for child in query:
            self.body(child)

########################################################################################################################
#              Детальные отчеты по цеху с номенклатурой                                                                #
########################################################################################################################


def rep_cex_working(request):
    one = Trep_cex_working(request)
    return HttpResponseRedirect(one.path_web)

def rep_cex_repair(request):
    one = Trep_cex_repair(request)
    return HttpResponseRedirect(one.path_web)


########################################################################################################################
#              Класс ведомость по цеху ремонтам                                                                        #
########################################################################################################################
class Trep_cex_repair():
    filename = u'%s_Цех_ремонт.xls'
    name_report = u'Отчет по ремонту по ТЭЦ '
    fieldname = 'repair'
    def __init__(self,request):
#        self.filename = 'speca_of_exp.xls'
        self.itogswork = []
        self.itogskind = []
        au = models.aUser.objects.get(user = request.user)
        if au.cex:
           self.cex = au.cex
        self.path_local = u'/home/plaksa/supplier/media/'
        self.path_web = u'http://172.27.80.127/supplier/media/'+self.__class__.filename % self.cex.name.replace('/','_').replace(" ","_")
        self.numpp = 1
        self.countcol = 7
        self.width_of_cols = [1200,10000,3000,3000,3000,5000,5000,5000]
        self.col2a = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.curr_row = 2
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet('Sheet1')
        self.clear_border()
        self.set_width()
        self.headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Кол-во',u'Цена',u'Сумма',]
        self.write_top()
        self.body()
        self.sheet.write(self.curr_row,1,u'Итого по отчету ',styles.stylebodytable,)
        list_cells = ''
        for one in self.itogswork:
            list_cells = list_cells +'+'+self.col2a[5]+str(one+1)
        if len(list_cells)>0:
            self.sheet.write(self.curr_row,5,xlwt.Formula(list_cells[1:]),styles.stylebodytable,)
        sss = self.path_local+self.__class__.filename % self.cex.name.replace('/','_').replace(" ","_")
        self.book.save(sss.encode('utf-8'))
#        self.book.save(self.path_local+self.__class__.filename % self.cex.name.replace('/','_').replace(" ","_"))
        self.book = None
##############################################################################################
#                             Запись шапки таблицы                                           #
##############################################################################################
    def write_top(self):
        self.sheet.row(self.curr_row).height = 500
        for col in range(0,len(self.headers)):
            self.sheet.write(self.curr_row,col,self.headers[col],styles.styletoptable,)
        self.curr_row += 1
##############################################################################################
#                             Процедура очистки обрамления колонок                           #
##############################################################################################
    def clear_border(self):
        for col in range(0,self.countcol-1):
            self.sheet.write(0,col,'',styles.styletop1)
        self.curr_row += 1
##############################################################################################
#                Процедура установки ширины колонок                                          #
##############################################################################################
    def set_width(self):
        for numcol in range(0,len(self.width_of_cols)):
            self.sheet.col(numcol).width = self.width_of_cols[numcol]

############################################################################
#            Рекурсивная процедура обхода tree_view дерева                 #
############################################################################
    def body(self):
        if self.cex==None:
            return
        self.sheet.write(self.curr_row,1,u'Цех '+self.cex.name,styles.s1,)
        self.curr_row += 1
        for kind in models.kind.objects.all().order_by('name'):
            data = models.register.objects.filter(cex = self.cex,ison = True,materials__kind__id=kind.id).aggregate(Sum('repair'))
            if (data['repair__sum'] == None) or (data['repair__sum'] == 0):
                continue
            self.sheet.write(self.curr_row,1,u'Категория '+kind.name,styles.s1,)
            self.curr_row += 1
            self.itogskind.append({'rowbeg':self.curr_row,'rowend':-1})
            for reg in models.register.objects.filter(cex = self.cex,ison = True,materials__kind__id=kind.id):
                self.sheet.write(self.curr_row,0,self.numpp,styles.stylebodytable,)
                self.sheet.write(self.curr_row,1,reg.materials.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,2,reg.materials.units.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,3,reg.repair,styles.stylebodytable,)
                self.sheet.write(self.curr_row,4,reg.materials.price,styles.stylebodytable,)
                self.sheet.write(self.curr_row,5,reg.sumrepair,styles.stylebodytable,)
                self.curr_row += 1
                self.numpp += 1
            self.itogskind[-1]['rowend']=self.curr_row
            self.sheet.write(self.curr_row,1,u'Итого по категории '+kind.name,styles.stylebodytable,)
            self.sheet.write(self.curr_row,5,xlwt.Formula(u'SUM('+self.col2a[5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                     u':'+self.col2a[5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
            self.curr_row += 1
        self.sheet.write(self.curr_row,1,u'Итого по цеху '+self.cex.name,styles.stylebodytable,)
        list_cells = ''
        for one in self.itogskind:
            list_cells = list_cells + '+'+self.col2a[5]+str(one['rowend']+1)
        if len(list_cells)>0:
            self.sheet.write(self.curr_row,5,xlwt.Formula(list_cells[1:]),styles.stylebodytable,)
        self.itogswork.append(self.curr_row)
        self.curr_row += 1

########################################################################################################################
#              Класс ведомость по цеху эксплуатация                                                                      #
########################################################################################################################
class Trep_cex_working():
    filename = u'%s_Цех_эксплуатация.xls'
    def __init__(self,request):
#        self.filename = 'speca_of_exp.xls'
        self.itogswork = []
        self.itogskind = []
        au = models.aUser.objects.get(user = request.user)
        if au.cex:
           self.cex = au.cex
        self.path_local = u'/home/plaksa/supplier/media/'
        self.path_web = u'http://172.27.80.127/supplier/media/'+self.__class__.filename % self.cex.name.replace('/','_').replace(" ","_")
        self.numpp = 1
        self.countcol = 7
        self.width_of_cols = [1200,10000,3000,3000,3000,5000,5000,5000]
        self.col2a = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.curr_row = 2
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet('Sheet1')
        self.clear_border()
        self.set_width()
        self.headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Кол-во',u'Цена',u'Сумма',]
        self.write_top()
        self.body()
        self.sheet.write(self.curr_row,1,u'Итого по отчету ',styles.stylebodytable,)
        list_cells = ''
        for one in self.itogswork:
            list_cells = list_cells +'+'+self.col2a[5]+str(one+1)
        if len(list_cells)>0:
            self.sheet.write(self.curr_row,5,xlwt.Formula(list_cells[1:]),styles.stylebodytable,)
        sss = self.path_local+self.__class__.filename % self.cex.name.replace('/','_').replace(" ","_")
        self.book.save(sss.encode('utf-8'))
        self.book = None
##############################################################################################
#                             Запись шапки таблицы                                           #
##############################################################################################
    def write_top(self):
        self.sheet.row(self.curr_row).height = 500
        for col in range(0,len(self.headers)):
            self.sheet.write(self.curr_row,col,self.headers[col],styles.styletoptable,)
        self.curr_row += 1
##############################################################################################
#                             Процедура очистки обрамления колонок                           #
##############################################################################################
    def clear_border(self):
        for col in range(0,self.countcol-1):
            self.sheet.write(0,col,'',styles.styletop1)
        self.curr_row += 1
##############################################################################################
#                Процедура установки ширины колонок                                          #
##############################################################################################
    def set_width(self):
        for numcol in range(0,len(self.width_of_cols)):
            self.sheet.col(numcol).width = self.width_of_cols[numcol]

############################################################################
#            Рекурсивная процедура обхода tree_view дерева                 #
############################################################################
    def body(self):
        if self.cex==None:
            return
        self.sheet.write(self.curr_row,1,u'Цех '+self.cex.name,styles.s1,)
        self.curr_row += 1
        for kind in models.kind.objects.all().order_by('name'):
            data = models.register.objects.filter(cex = self.cex,ison = True,materials__kind__id=kind.id).aggregate(Sum('working'))
            if (data['working__sum'] == None) or (data['working__sum'] == 0):
                continue
            self.sheet.write(self.curr_row,1,u'Категория '+kind.name,styles.s1,)
            self.curr_row += 1
            self.itogskind.append({'rowbeg':self.curr_row,'rowend':-1})
            for reg in models.register.objects.filter(cex = self.cex,ison = True,materials__kind__id=kind.id):
                self.sheet.write(self.curr_row,0,self.numpp,styles.stylebodytable,)
                self.sheet.write(self.curr_row,1,reg.materials.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,2,reg.materials.units.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,3,reg.working,styles.stylebodytable,)
                self.sheet.write(self.curr_row,4,reg.materials.price,styles.stylebodytable,)
                self.sheet.write(self.curr_row,5,reg.sumworking,styles.stylebodytable,)
                self.curr_row += 1
                self.numpp += 1
            self.itogskind[-1]['rowend']=self.curr_row
            self.sheet.write(self.curr_row,1,u'Итого по категории '+kind.name,styles.stylebodytable,)
            self.sheet.write(self.curr_row,5,xlwt.Formula(u'SUM('+self.col2a[5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                     u':'+self.col2a[5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
            self.curr_row += 1
        self.sheet.write(self.curr_row,1,u'Итого по цеху '+self.cex.name,styles.stylebodytable,)
        list_cells = ''
        for one in self.itogskind:
            list_cells = list_cells + '+'+self.col2a[5]+str(one['rowend']+1)
        if len(list_cells)>0:
            self.sheet.write(self.curr_row,5,xlwt.Formula(list_cells[1:]),styles.stylebodytable,)
        self.itogswork.append(self.curr_row)
        self.curr_row += 1



########################################################################################################################
#                   Ведомость по цеху cex эксплуатация с разбивкой по месяцам                               #
########################################################################################################################
#import copy
from datetime import datetime
def rep_cex_month_working(request):
    one = Trep_cex_month_working(request)
    return HttpResponseRedirect(one.path_web)

########################################################################################################################
#                   Ведомость по цеху cex ремонт с разбивкой по месяцам                                     #
########################################################################################################################
def rep_cex_month_repair(request):
    one = Trep_cex_month_repair(request)
    return HttpResponseRedirect(one.path_web)

########################################################################################################################
#            CLASS  Ведомость по цеху эксплуатация с разбивкой по месяцам                                              #
########################################################################################################################
from datetime import datetime
import gc
class Trep_cex_month_working():
    filename = u'%s_Эксплуатация_по_месяцам_по_цеху.xls'
    name_report = u'Отчет по эксплуатации по цеху '
    fieldname = 'working'
    def __init__(self,request):
        self.itogskind = []
        au = models.aUser.objects.get(user = request.user)
        if au.cex:
           self.cex = au.cex
        self.path_local = u'/home/plaksa/supplier/media/'
        self.path_web = u'http://172.27.80.127/supplier/media/'+self.__class__.filename % self.cex.name.replace('/','_').replace(" ","_")
        self.numpp = 1
        self.countcol = 7
        self.width_of_cols = [1200,10000,3000,3000,3000,3000,3000,3000]
        self.col2a = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                     'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ']
        self.curr_row = 2
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet('Sheet1')
        self.clear_border()
        self.set_width()
        self.headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Цена',u'Кол-во год',u'Сумма год',u'Кол-во 1',u'Сумма 1',u'Кол-во 2',u'Сумма 2'
                        ,u'Кол-во 3',u'Сумма 3',u'Кол-во 4',u'Сумма 4',u'Кол-во 5',u'Сумма 5',u'Кол-во 6',u'Сумма 6',u'Кол-во 7',u'Сумма 7'
                        ,u'Кол-во 8',u'Сумма 8',u'Кол-во 9',u'Сумма 9',u'Кол-во 10',u'Сумма 10',u'Кол-во 11',u'Сумма 11',u'Кол-во 12',u'Сумма 12']
        self.write_top()
        self.body()
        sss = self.path_local+self.__class__.filename % self.cex.name.replace('/','_').replace(" ","_")
        self.book.save(sss.encode('utf-8'))
##############################################################################################
#                             Запись шапки таблицы                                           #
##############################################################################################
    def write_top(self):
        self.sheet.write(self.curr_row,1,self.__class__.name_report+self.cex.name+u' дата формирования '+str(datetime.now()),styles.s1,)
        self.curr_row += 1
        self.sheet.row(self.curr_row).height = 500
        for col in range(0,len(self.headers)):
            self.sheet.write(self.curr_row,col,self.headers[col],styles.styletoptable,)
        self.curr_row += 1
##############################################################################################
#                             Процедура очистки обрамления колонок                           #
##############################################################################################
    def clear_border(self):
        for col in range(0,self.countcol-1):
            self.sheet.write(0,col,'',styles.styletop1)
        self.curr_row += 1
##############################################################################################
#                Процедура установки ширины колонок                                          #
##############################################################################################
    def set_width(self):
        for numcol in range(0,len(self.width_of_cols)):
            self.sheet.col(numcol).width = self.width_of_cols[numcol]

##############################################################################################
#                Функция формирования строки для формулы                                     #
##############################################################################################
    def cells_to_itog(self,namecol,lst):
        s = ''
        for one in lst:
            s = s + '+'+namecol+str(one['rowend']+1)
        return s[1:]
############################################################################
#            Рекурсивная процедура обхода tree_view дерева                 #
############################################################################
    def body(self):
        if self.cex==None:
            return
#      Цикл по справочнику категорий материалов - kind
        for kind in models.kind.objects.all().order_by('name'):
            data = models.register.objects.filter(cex = self.cex,ison = True,materials__kind__id=kind.id).aggregate(Sum(self.__class__.fieldname))
            if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                continue
            self.sheet.write(self.curr_row,1,u'Категория '+kind.name,styles.s1,)
            self.curr_row += 1
            self.itogskind.append({'rowbeg':self.curr_row,'rowend':-1})
#          Цикл по справочнику материалов ТМЦ - materials
            for mat in models.materials.objects.filter(kind = kind.id):
                data = models.register.objects.filter(cex = self.cex,ison = True,materials=mat.id).aggregate(Sum(self.__class__.fieldname))
                if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                    continue
                sum_months = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
#              Цикл по реестру  - register
                for reg in models.register.objects.filter(cex = self.cex,ison = True,materials = mat.id):
                    sum_months[reg.datesupply.month] = sum_months[reg.datesupply.month] + getattr(reg,self.__class__.fieldname)
                self.sheet.write(self.curr_row,0,self.numpp,styles.stylebodytable,)
                self.sheet.write(self.curr_row,1,mat.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,2,mat.units.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,3,mat.price,styles.stylebodytable,)
                for month in range(1,13):
                    self.sheet.write(self.curr_row,month*2+4,sum_months[month],styles.stylebodytable,)
                    self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(self.col2a[month*2+4]+str(self.curr_row+1)+u'*'+ \
                                     self.col2a[3]+str(self.curr_row+1)),styles.stylebodytable,)

                self.sheet.write(self.curr_row,4,xlwt.Formula(self.col2a[6]+str(self.curr_row+1)+u'+'+self.col2a[8]+str(self.curr_row+1)+u'+' \
                    +self.col2a[10]+str(self.curr_row+1)+u'+'+self.col2a[12]+str(self.curr_row+1)+u'+' \
                    +self.col2a[14]+str(self.curr_row+1)+u'+'+self.col2a[16]+str(self.curr_row+1)+u'+' \
                    +self.col2a[18]+str(self.curr_row+1)+u'+'+self.col2a[20]+str(self.curr_row+1)+u'+' \
                    +self.col2a[22]+str(self.curr_row+1)+u'+'+self.col2a[24]+str(self.curr_row+1)+u'+' \
                    +self.col2a[26]+str(self.curr_row+1)+u'+'+self.col2a[28]+str(self.curr_row+1)),styles.stylebodytable,)
                self.sheet.write(self.curr_row,5,xlwt.Formula(self.col2a[3]+str(self.curr_row+1)+u'*'+ \
                     self.col2a[4]+str(self.curr_row+1)),styles.stylebodytable,)
                self.curr_row += 1
                self.numpp += 1
#            итоги по категории
            self.itogskind[-1]['rowend']=self.curr_row
            self.sheet.write(self.curr_row,1,u'Итого по категории '+kind.name,styles.stylebodytable,)
            self.sheet.write(self.curr_row,5,xlwt.Formula(u'SUM('+self.col2a[5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                     u':'+self.col2a[5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
            for month in range(1,13):
                self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(u'SUM('+self.col2a[month*2+5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                     u':'+self.col2a[month*2+5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
            self.curr_row += 1
#       Итоги по цеху
        self.sheet.write(self.curr_row,1,u'Итого по цеху '+self.cex.name,styles.stylebodytable,)
        if len(self.itogskind)>0:
            for month in range(0,13):
                self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(self.cells_to_itog(self.col2a[month*2+5],self.itogskind)),styles.stylebodytable,)
########################################################################################################################
#            CLASS  Ведомость по ТЭЦ ремонты с разбивкой по месяцам                                                   #
########################################################################################################################
class Trep_cex_month_repair(Trep_cex_month_working):
    filename = u'%s_Ремонт_по_месяцам_по_цеху.xls'
    fieldname = 'repair'
    name_report = u'Отчет по ремонтам по цеху '


########################################################################################################################
#                   Ведомость по предприятию factory эксплуатация с разбивкой по месяцам                               #
########################################################################################################################
def rep_fac_month_working(request,id = None):
    one = Trep_fac_month_working(request,id)
    return HttpResponseRedirect(one.path_web)

########################################################################################################################
#                   Ведомость по предприятию factory ремонт с разбивкой по месяцам                                     #
########################################################################################################################
def rep_fac_month_repair(request,id = None):
    one = Trep_fac_month_repair(request,id)
    return HttpResponseRedirect(one.path_web)

########################################################################################################################
#                   Ведомость по предприятию factory эксплуатация без разбивки по месяцам                              #
########################################################################################################################
def rep_fac_working(request,id = None):
    one = Trep_fac_working(request,id)
    return HttpResponseRedirect(one.path_web)

########################################################################################################################
#                   Ведомость по предприятию factory ремонт без разбивки по месяцам                                    #
########################################################################################################################
def rep_fac_repair(request,id = None):
    one = Trep_fac_repair(request,id)
    return HttpResponseRedirect(one.path_web)



########################################################################################################################
#            CLASS  Ведомость по предприятию эксплуатация с разбивкой по месяцам                                              #
########################################################################################################################
from datetime import datetime
class Trep_fac_month_working():
    filename = u'%s_Эксплуатация_по_месяцам_по_ТЭЦ.xls'
    name_report = u'Отчет по эксплуатации по ТЭЦ '
    fieldname = 'working'
    headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Цена',u'Кол-во год',u'Сумма год',u'Кол-во 1',u'Сумма 1',u'Кол-во 2',u'Сумма 2'
                        ,u'Кол-во 3',u'Сумма 3',u'Кол-во 4',u'Сумма 4',u'Кол-во 5',u'Сумма 5',u'Кол-во 6',u'Сумма 6',u'Кол-во 7',u'Сумма 7'
                        ,u'Кол-во 8',u'Сумма 8',u'Кол-во 9',u'Сумма 9',u'Кол-во 10',u'Сумма 10',u'Кол-во 11',u'Сумма 11',u'Кол-во 12',u'Сумма 12']
#    fieldinst = models.reg.working
    def __init__(self,request,id = None):
#        self.filename = 'speca_of_exp.xls'
        self.itogskind = []
        self.itogscex = []
        au = models.aUser.objects.get(user = request.user)
        if au.cex:
           self.factory = au.cex.factory
        else:
           if id != None:
               self.factory = models.factory.objects.get(pk = id)
           else:
               return
        self.path_local = u'/home/plaksa/supplier/media/'
        self.path_web = u'http://172.27.80.127/supplier/media/'+self.__class__.filename % self.factory.name.replace('/','_').replace(" ","_")
        self.numpp = 1
        self.countcol = 7
        self.width_of_cols = [1200,10000,3000,3000,3000,3000,3000,3000]
        self.col2a = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                     'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ']
        self.curr_row = 2
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet('Sheet1')
        self.clear_border()
        self.set_width()

        self.headers = self.__class__.headers
        self.write_top()
        self.body()
        sss = self.path_local+self.__class__.filename % self.factory.name.replace('/','_').replace(" ","_")
        self.book.save(sss.encode('utf-8'))
        self.book = None
##############################################################################################
#                             Запись шапки таблицы                                           #
##############################################################################################
    def write_top(self):
        self.sheet.write(self.curr_row,1,self.__class__.name_report+self.factory.name+u' дата формирования '+str(datetime.now()),styles.s1,)
        self.curr_row += 1
        self.sheet.row(self.curr_row).height = 500
        for col in range(0,len(self.headers)):
            self.sheet.write(self.curr_row,col,self.headers[col],styles.styletoptable,)
        self.curr_row += 1
##############################################################################################
#                             Процедура очистки обрамления колонок                           #
##############################################################################################
    def clear_border(self):
        for col in range(0,self.countcol-1):
            self.sheet.write(0,col,'',styles.styletop1)
        self.curr_row += 1
##############################################################################################
#                Процедура установки ширины колонок                                          #
##############################################################################################
    def set_width(self):
        for numcol in range(0,len(self.width_of_cols)):
            self.sheet.col(numcol).width = self.width_of_cols[numcol]

##############################################################################################
#                Функция формирования строки для формулы                                     #
##############################################################################################
    def cells_to_itog(self,namecol,lst):
        s = ''
        for one in lst:
            s = s + '+'+namecol+str(one['rowend']+1)
        return s[1:]
############################################################################
#            Рекурсивная процедура обхода tree_view дерева                 #
############################################################################
    def body(self):
        if self.factory==None:
            return
#      Цикл по справочнику цехов предприятия - cex
        for cex in models.cex.objects.filter(factory = self.factory):
            data = models.register.objects.filter(cex = cex,ison = True).aggregate(Sum(self.__class__.fieldname))
            if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                continue
            self.sheet.write(self.curr_row,1,u'Цех '+cex.name,styles.s1,)
            self.curr_row += 1
            self.itogskind = []
#      Цикл по справочнику категорий материалов - kind
            for kind in models.kind.objects.all().order_by('name'):
                data = models.register.objects.filter(cex = cex,ison = True,materials__kind__id=kind.id).aggregate(Sum(self.__class__.fieldname))
                if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                    continue
                self.sheet.write(self.curr_row,1,u'Категория '+kind.name,styles.s1,)
                self.curr_row += 1
                self.itogskind.append({'rowbeg':self.curr_row,'rowend':-1})
#              Цикл по справочнику материалов ТМЦ - materials
                for mat in models.materials.objects.filter(kind = kind.id):
                    data = models.register.objects.filter(cex = cex,ison = True,materials=mat.id).aggregate(Sum(self.__class__.fieldname))
                    if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                        continue
                    sum_months = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
#                  Цикл по реестру  - register
                    for reg in models.register.objects.filter(cex = cex,ison = True,materials = mat.id):
#                        print getattr(reg,self.__class__.fieldname)
                        sum_months[reg.datesupply.month] = sum_months[reg.datesupply.month] + getattr(reg,self.__class__.fieldname)
#                         self.__class__.fieldinst
#                        reg.working
                    self.sheet.write(self.curr_row,0,self.numpp,styles.stylebodytable,)
                    self.sheet.write(self.curr_row,1,mat.name,styles.stylebodytable,)
                    self.sheet.write(self.curr_row,2,mat.units.name,styles.stylebodytable,)
                    self.sheet.write(self.curr_row,3,mat.price,styles.stylebodytable,)
                    for month in range(1,13):
                        self.sheet.write(self.curr_row,month*2+4,sum_months[month],styles.stylebodytable,)
                        self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(self.col2a[month*2+4]+str(self.curr_row+1)+u'*'+ \
                                         self.col2a[3]+str(self.curr_row+1)),styles.stylebodytable,)
                    self.sheet.write(self.curr_row,4,xlwt.Formula(self.col2a[6]+str(self.curr_row+1)+u'+'+self.col2a[8]+str(self.curr_row+1)+u'+' \
                        +self.col2a[10]+str(self.curr_row+1)+u'+'+self.col2a[12]+str(self.curr_row+1)+u'+' \
                        +self.col2a[14]+str(self.curr_row+1)+u'+'+self.col2a[16]+str(self.curr_row+1)+u'+' \
                        +self.col2a[18]+str(self.curr_row+1)+u'+'+self.col2a[20]+str(self.curr_row+1)+u'+' \
                        +self.col2a[22]+str(self.curr_row+1)+u'+'+self.col2a[24]+str(self.curr_row+1)+u'+' \
                        +self.col2a[26]+str(self.curr_row+1)+u'+'+self.col2a[28]+str(self.curr_row+1)),styles.stylebodytable,)
                    self.sheet.write(self.curr_row,5,xlwt.Formula(self.col2a[3]+str(self.curr_row+1)+u'*'+ \
                         self.col2a[4]+str(self.curr_row+1)),styles.stylebodytable,)
                    self.curr_row += 1
                    self.numpp += 1
#                итоги по категории
                self.itogskind[-1]['rowend']=self.curr_row
                self.sheet.write(self.curr_row,1,u'Итого по категории '+kind.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,5,xlwt.Formula(u'SUM('+self.col2a[5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                         u':'+self.col2a[5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
                for month in range(1,13):
                    self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(u'SUM('+self.col2a[month*2+5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                         u':'+self.col2a[month*2+5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
                self.curr_row += 1
#           Итоги по цеху
            self.sheet.write(self.curr_row,1,u'Итого по цеху '+cex.name,styles.stylebodytable,)
            if len(self.itogskind)>0:
                for month in range(0,13):
                    self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(self.cells_to_itog(self.col2a[month*2+5],self.itogskind)),styles.stylebodytable,)
            one = {'rowend':self.curr_row}
            self.itogscex.append(one)
            self.curr_row += 1
#        Итоги по отчету
        self.sheet.write(self.curr_row,1,u'Итого по отчету ',styles.stylebodytable,)
        if len(self.itogscex)>0:
                for month in range(0,13):
                    self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(self.cells_to_itog(self.col2a[month*2+5],self.itogscex)),styles.stylebodytable,)

########################################################################################################################
#            CLASS  Ведомость по ТЭЦ ремонты с разбивкой по месяцам                                                   #
########################################################################################################################
class Trep_fac_month_repair(Trep_fac_month_working):
    filename = u'%s_Ремонт_по_месяцам_по_ТЭЦ.xls'
    fieldname = 'repair'
    name_report = u'Отчет по ремонтам по ТЭЦ '


########################################################################################################################
#            CLASS  Ведомость полная по эксплуатация с разбивкой по месяцам                                              #
########################################################################################################################
from datetime import datetime
import gc
class Trep_all_month_working():
    filename = u'%s_Эксплуатация_по_месяцам_полная.xls'
    name_report = u'Отчет по эксплуатации с помесячной разбивкой по ЧГ'
    fieldname = 'working'
    headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Цена',u'Кол-во год',u'Сумма год',u'Кол-во 1',u'Сумма 1',u'Кол-во 2',u'Сумма 2'
                        ,u'Кол-во 3',u'Сумма 3',u'Кол-во 4',u'Сумма 4',u'Кол-во 5',u'Сумма 5',u'Кол-во 6',u'Сумма 6',u'Кол-во 7',u'Сумма 7'
                        ,u'Кол-во 8',u'Сумма 8',u'Кол-во 9',u'Сумма 9',u'Кол-во 10',u'Сумма 10',u'Кол-во 11',u'Сумма 11',u'Кол-во 12',u'Сумма 12']
#    fieldinst = models.reg.working
    def __init__(self,request):
#        self.filename = 'speca_of_exp.xls'
        self.itogskind = []
        self.itogscex = []
        self.itogsfac = []
        self.path_local = u'/home/plaksa/supplier/media/'
        self.path_web = u'http://172.27.80.127/supplier/media/'+self.__class__.filename % u'_полная'
        self.numpp = 1
        self.countcol = 7
        self.width_of_cols = [1200,10000,3000,3000,3000,3000,3000,3000]
        self.col2a = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                     'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ']
        self.curr_row = 2
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet('Sheet1')
        self.clear_border()
        self.set_width()
#       self.headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Цена',u'Кол-во год',u'Сумма год',u'Кол-во 1',u'Сумма 1',u'Кол-во 2',u'Сумма 2'
#                       ,u'Кол-во 3',u'Сумма 3',u'Кол-во 4',u'Сумма 4',u'Кол-во 5',u'Сумма 5',u'Кол-во 6',u'Сумма 6',u'Кол-во 7',u'Сумма 7'
#                       ,u'Кол-во 8',u'Сумма 8',u'Кол-во 9',u'Сумма 9',u'Кол-во 10',u'Сумма 10',u'Кол-во 11',u'Сумма 11',u'Кол-во 12',u'Сумма 12']
        self.headers = self.__class__.headers
        self.write_top()
        self.body()
        sss = self.path_local+self.__class__.filename % u'_полная'
        self.book.save(sss.encode('utf-8'))
        self.book = None
        gc.collect()

##############################################################################################
#                             Запись шапки таблицы                                           #
##############################################################################################
    def write_top(self):
        self.sheet.write(self.curr_row,1,self.__class__.name_report+u' полная '+u' дата формирования '+str(datetime.now()),styles.s1,)
        self.curr_row += 1
        self.sheet.row(self.curr_row).height = 500
        for col in range(0,len(self.headers)):
            self.sheet.write(self.curr_row,col,self.headers[col],styles.styletoptable,)
        self.curr_row += 1
##############################################################################################
#                             Процедура очистки обрамления колонок                           #
##############################################################################################
    def clear_border(self):
        for col in range(0,self.countcol-1):
            self.sheet.write(0,col,'',styles.styletop1)
        self.curr_row += 1
##############################################################################################
#                Процедура установки ширины колонок                                          #
##############################################################################################
    def set_width(self):
        for numcol in range(0,len(self.width_of_cols)):
            self.sheet.col(numcol).width = self.width_of_cols[numcol]

##############################################################################################
#                Функция формирования строки для формулы                                     #
##############################################################################################
    def cells_to_itog(self,namecol,lst):
        s = ''
        for one in lst:
            s = s + '+'+namecol+str(one['rowend']+1)
        return s[1:]
############################################################################
#            Рекурсивная процедура обхода tree_view дерева                 #
############################################################################
    def body(self):
#      Цикл по справочнику предприятий - factory
        for fac in models.factory.objects.all():
#   #      Цикл по справочнику цехов предприятия - cex
            for cex in models.cex.objects.filter(factory = fac):
                data = models.register.objects.filter(cex = cex,ison = True).aggregate(Sum(self.__class__.fieldname))
                if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                    continue
                self.sheet.write(self.curr_row,1,u'Цех '+cex.name,styles.s1,)
                self.curr_row += 1
                self.itogskind = []
#   #      Цикл по справочнику категорий материалов - kind
                for kind in models.kind.objects.all().order_by('name'):
                    data = models.register.objects.filter(cex = cex,ison = True,materials__kind__id=kind.id).aggregate(Sum(self.__class__.fieldname))
                    if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                        continue
                    self.sheet.write(self.curr_row,1,u'Категория '+kind.name,styles.s1,)
                    self.curr_row += 1
                    self.itogskind.append({'rowbeg':self.curr_row,'rowend':-1})
#   #              Цикл по справочнику материалов ТМЦ - materials
                    for mat in models.materials.objects.filter(kind = kind.id):
                        data = models.register.objects.filter(cex = cex,ison = True,materials=mat.id).aggregate(Sum(self.__class__.fieldname))
                        if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                            continue
                        sum_months = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
#   #                  Цикл по реестру  - register
                        for reg in models.register.objects.filter(cex = cex,ison = True,materials = mat.id):
                            sum_months[reg.datesupply.month] = sum_months[reg.datesupply.month] + getattr(reg,self.__class__.fieldname)
                        self.sheet.write(self.curr_row,0,self.numpp,styles.stylebodytable,)
                        self.sheet.write(self.curr_row,1,mat.name,styles.stylebodytable,)
                        self.sheet.write(self.curr_row,2,mat.units.name,styles.stylebodytable,)
                        self.sheet.write(self.curr_row,3,mat.price,styles.stylebodytable,)
                        for month in range(1,13):
                            self.sheet.write(self.curr_row,month*2+4,sum_months[month],styles.stylebodytable,)
                            self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(self.col2a[month*2+4]+str(self.curr_row+1)+u'*'+ \
                                             self.col2a[3]+str(self.curr_row+1)),styles.stylebodytable,)
                        self.sheet.write(self.curr_row,4,xlwt.Formula(self.col2a[6]+str(self.curr_row+1)+u'+'+self.col2a[8]+str(self.curr_row+1)+u'+' \
                            +self.col2a[10]+str(self.curr_row+1)+u'+'+self.col2a[12]+str(self.curr_row+1)+u'+' \
                            +self.col2a[14]+str(self.curr_row+1)+u'+'+self.col2a[16]+str(self.curr_row+1)+u'+' \
                            +self.col2a[18]+str(self.curr_row+1)+u'+'+self.col2a[20]+str(self.curr_row+1)+u'+' \
                            +self.col2a[22]+str(self.curr_row+1)+u'+'+self.col2a[24]+str(self.curr_row+1)+u'+' \
                            +self.col2a[26]+str(self.curr_row+1)+u'+'+self.col2a[28]+str(self.curr_row+1)),styles.stylebodytable,)
                        self.sheet.write(self.curr_row,5,xlwt.Formula(self.col2a[3]+str(self.curr_row+1)+u'*'+ \
                             self.col2a[4]+str(self.curr_row+1)),styles.stylebodytable,)
                        self.curr_row += 1
                        self.numpp += 1
#   #                итоги по категории
                    self.itogskind[-1]['rowend']=self.curr_row
                    self.sheet.write(self.curr_row,1,u'Итого по категории '+kind.name,styles.stylebodytable,)
                    self.sheet.write(self.curr_row,5,xlwt.Formula(u'SUM('+self.col2a[5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                             u':'+self.col2a[5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
                    for month in range(1,13):
                        self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(u'SUM('+self.col2a[month*2+5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                             u':'+self.col2a[month*2+5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
                    self.curr_row += 1
#   #           Итоги по цеху
                self.sheet.write(self.curr_row,1,u'Итого по цеху '+cex.name,styles.stylebodytable,)
                if len(self.itogskind)>0:
                    for month in range(0,13):
                        self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(self.cells_to_itog(self.col2a[month*2+5],self.itogskind)),styles.stylebodytable,)
                one = {'rowend':self.curr_row}
                self.itogscex.append(one)
                self.curr_row += 1
#   #        Итоги по предприятию
            self.sheet.write(self.curr_row,1,u'Итого по предприятию '+fac.name,styles.stylebodytable,)
            if len(self.itogscex)>0:
                    for month in range(0,13):
                        self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(self.cells_to_itog(self.col2a[month*2+5],self.itogscex)),styles.stylebodytable,)
            one = {'rowend':self.curr_row}
            self.itogsfac.append(one)
            self.curr_row += 1
#     Итоги по предприятию
        self.sheet.write(self.curr_row,1,u'Итого по отчету ',styles.stylebodytable,)
        if len(self.itogsfac)>0:
            for month in range(0,13):
                self.sheet.write(self.curr_row,month*2+5,xlwt.Formula(self.cells_to_itog(self.col2a[month*2+5],self.itogsfac)),styles.stylebodytable,)

########################################################################################################################
#                   Ведомость полная эксплуатация с разбивкой по месяцам                                               #
########################################################################################################################
def rep_all_month_working(request):
    one = Trep_all_month_working(request)
    path_web = one.path_web
    one = None
    return HttpResponseRedirect(path_web)

########################################################################################################################
#            CLASS  Ведомость полная по ремонтам с разбивкой по месяцам                                                #
########################################################################################################################
from datetime import datetime
class Trep_all_month_repair(Trep_all_month_working):
    filename = u'%s_Ремонты_по_месяцам_полная.xls'
    name_report = u'Отчет по ремонтам полный '
    fieldname = 'repair'

########################################################################################################################
#                   Ведомость полная эксплуатация с разбивкой по месяцам                                               #
########################################################################################################################
def rep_all_month_repair(request):
    one = Trep_all_month_repair(request)
    path_web = one.path_web
    one = None
    return HttpResponseRedirect(path_web)

########################################################################################################################
#                   Ведомость полная эксплуатация                                                                      #
########################################################################################################################
def rep_all_working(request):
    one = Trep_all_working(request)
    return HttpResponseRedirect(one.path_web)

########################################################################################################################
#                   Ведомость полная ремонт                                                                            #
########################################################################################################################
def rep_all_repair(request):
    one = Trep_all_repair(request)
    return HttpResponseRedirect(one.path_web)

########################################################################################################################
#            CLASS  Ведомость полная по эксплуатация без разбивки по месяцам                                           #
########################################################################################################################
from datetime import datetime
class Trep_all_working(Trep_all_month_working):
    name_report = u'Отчет по эксплуатации ЧГ '
    filename = u'%s_Эксплуатация_ЧГ.xls'
    fieldname = 'working'
    headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Цена',u'Кол-во',u'Сумма']
#    fieldinst = models.reg.working

########################################################################################################################
#            CLASS  Ведомость полная по ремонту без разбивки по месяцам                                                #
########################################################################################################################
from datetime import datetime
class Trep_all_repair(Trep_all_working):
    name_report = u'Отчет по ремонту ЧГ '
    filename = u'%s_ремонт_ЧГ.xls'
    fieldname = 'repair'
    headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Цена',u'Кол-во',u'Сумма']

############################################################################
#            Рекурсивная процедура обхода tree_view дерева                 #
############################################################################
    def body(self):
#      Цикл по справочнику предприятий - factory
        for fac in models.factory.objects.all():
            self.itogscex = []
#   #      Цикл по справочнику цехов предприятия - cex
            for cex in models.cex.objects.filter(factory = fac):
                data = models.register.objects.filter(cex = cex,ison = True).aggregate(Sum(self.__class__.fieldname))
                if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                    continue
                self.sheet.write(self.curr_row,1,u'Цех '+cex.name,styles.s1,)
                self.curr_row += 1
                self.itogskind = []
#   #      Цикл по справочнику категорий материалов - kind
                for kind in models.kind.objects.all().order_by('name'):
                    data = models.register.objects.filter(cex = cex,ison = True,materials__kind__id=kind.id).aggregate(Sum(self.__class__.fieldname))
                    if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                        continue
                    self.sheet.write(self.curr_row,1,u'Категория '+kind.name,styles.s1,)
                    self.curr_row += 1
                    self.itogskind.append({'rowbeg':self.curr_row,'rowend':-1})
#   #              Цикл по справочнику материалов ТМЦ - materials
                    for mat in models.materials.objects.filter(kind = kind.id):
                        data = models.register.objects.filter(cex = cex,ison = True,materials=mat.id).aggregate(Sum(self.__class__.fieldname))
                        if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                            continue
#   #                  Цикл по реестру  - register
                        self.sheet.write(self.curr_row,0,self.numpp,styles.stylebodytable)
                        self.sheet.write(self.curr_row,1,mat.name,styles.stylebodytable)
                        self.sheet.write(self.curr_row,2,mat.units.name,styles.stylebodytable)
                        self.sheet.write(self.curr_row,3,mat.price,styles.stylebodytable)
                        self.sheet.write(self.curr_row,4,data[self.__class__.fieldname+'__sum'],styles.stylebodytable)
                        self.sheet.write(self.curr_row,5,xlwt.Formula(self.col2a[3]+str(self.curr_row+1)+u'*'+ self.col2a[4]+str(self.curr_row+1)),styles.stylebodytable)
                        self.curr_row += 1
                        self.numpp += 1
#   #                итоги по категории
                    self.itogskind[-1]['rowend']=self.curr_row
                    self.sheet.write(self.curr_row,1,u'Итого по категории '+kind.name,styles.stylebodytable,)
                    self.sheet.write(self.curr_row,5,xlwt.Formula(u'SUM('+self.col2a[5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                             u':'+self.col2a[5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
                    self.curr_row += 1
#   #           Итоги по цеху
                self.sheet.write(self.curr_row,1,u'Итого по цеху '+cex.name,styles.stylebodytable,)
                if len(self.itogskind)>0:
                    self.sheet.write(self.curr_row,5,xlwt.Formula(self.cells_to_itog(self.col2a[5],self.itogskind)),styles.stylebodytable)
                one = {'rowend':self.curr_row}
                self.itogscex.append(one)
                self.curr_row += 1
#   #        Итоги по предприятию
            self.sheet.write(self.curr_row,1,u'Итого по предприятию '+fac.name,styles.stylebodytable,)
            if len(self.itogscex)>0:
                self.sheet.write(self.curr_row,5,xlwt.Formula(self.cells_to_itog(self.col2a[5],self.itogscex)),styles.stylebodytable,)
            one = {'rowend':self.curr_row}
            self.itogsfac.append(one)
            self.curr_row += 1
#     Итоги по отчету
        self.sheet.write(self.curr_row,1,u'Итого по отчету ',styles.stylebodytable,)
        if len(self.itogsfac)>0:
            self.sheet.write(self.curr_row,5,xlwt.Formula(self.cells_to_itog(self.col2a[5],self.itogsfac)),styles.stylebodytable,)

########################################################################################################################
#            CLASS  Ведомость по предприятию эксплуатация без разбивки по месяцам                                      #
########################################################################################################################
from datetime import datetime
class Trep_fac_working(Trep_fac_month_working):
    filename = u'%s_Эксплуатация_ТЭЦ.xls'
    name_report = u'Отчет по эксплуатации по ТЭЦ '
    fieldname = 'working'
    headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Цена',u'Кол-во',u'Сумма']
############################################################################
#            Рекурсивная процедура обхода tree_view дерева                 #
############################################################################
    def body(self):
        if self.factory==None:
            return
#      Цикл по справочнику цехов предприятия - cex
        for cex in models.cex.objects.filter(factory = self.factory):
            data = models.register.objects.filter(cex = cex,ison = True).aggregate(Sum(self.__class__.fieldname))
            if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                continue
            self.sheet.write(self.curr_row,1,u'Цех '+cex.name,styles.s1,)
            self.curr_row += 1
            self.itogskind = []
#      Цикл по справочнику категорий материалов - kind
            for kind in models.kind.objects.all().order_by('name'):
                data = models.register.objects.filter(cex = cex,ison = True,materials__kind__id=kind.id).aggregate(Sum(self.__class__.fieldname))
                if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                    continue
                self.sheet.write(self.curr_row,1,u'Категория '+kind.name,styles.s1,)
                self.curr_row += 1
                self.itogskind.append({'rowbeg':self.curr_row,'rowend':-1})
#              Цикл по справочнику материалов ТМЦ - materials
                for mat in models.materials.objects.filter(kind = kind.id):
                    data = models.register.objects.filter(cex = cex,ison = True,materials=mat.id).aggregate(Sum(self.__class__.fieldname))
                    if (data[self.__class__.fieldname+'__sum'] == None) or (data[self.__class__.fieldname+'__sum'] == 0):
                        continue
                    self.sheet.write(self.curr_row,0,self.numpp,styles.stylebodytable)
                    self.sheet.write(self.curr_row,1,mat.name,styles.stylebodytable)
                    self.sheet.write(self.curr_row,2,mat.units.name,styles.stylebodytable)
                    self.sheet.write(self.curr_row,3,mat.price,styles.stylebodytable)
                    self.sheet.write(self.curr_row,4,data[self.__class__.fieldname+'__sum'],styles.stylebodytable)
                    self.sheet.write(self.curr_row,5,xlwt.Formula(self.col2a[3]+str(self.curr_row+1)+u'*'+ self.col2a[4]+str(self.curr_row+1)),styles.stylebodytable)
                    self.curr_row += 1
                    self.numpp += 1
#                итоги по категории
                self.itogskind[-1]['rowend']=self.curr_row
                self.sheet.write(self.curr_row,1,u'Итого по категории '+kind.name,styles.stylebodytable,)
                self.sheet.write(self.curr_row,5,xlwt.Formula(u'SUM('+self.col2a[5]+str(self.itogskind[-1]['rowbeg']+1)+ \
                         u':'+self.col2a[5]+str(self.itogskind[-1]['rowend'])+u')'),styles.stylebodytable,)
                self.curr_row += 1
#           Итоги по цеху
            self.sheet.write(self.curr_row,1,u'Итого по цеху '+cex.name,styles.stylebodytable,)
            if len(self.itogskind)>0:
                self.sheet.write(self.curr_row,5,xlwt.Formula(self.cells_to_itog(self.col2a[5],self.itogskind)),styles.stylebodytable)
            one = {'rowend':self.curr_row}
            self.itogscex.append(one)
            self.curr_row += 1
#        Итоги по отчету
        self.sheet.write(self.curr_row,1,u'Итого по отчету ',styles.stylebodytable,)
        if len(self.itogscex)>0:
            self.sheet.write(self.curr_row,5,xlwt.Formula(self.cells_to_itog(self.col2a[5],self.itogscex)),styles.stylebodytable,)


########################################################################################################################
#            CLASS  Ведомость по предприятию ремонт без разбивки по месяцам                                      #
########################################################################################################################
from datetime import datetime
class Trep_fac_repair(Trep_fac_working):
    filename = u'%s_Ремонт_ТЭЦ.xls'
    name_report = u'Отчет по ремонту по ТЭЦ '
    fieldname = 'repair'
    headers = [u'№ пп',u'Наименование',u'Ед.Изм.',u'Цена',u'Кол-во',u'Сумма']

