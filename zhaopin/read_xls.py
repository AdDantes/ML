import xlrd
import openpyxl

data = xlrd.open_workbook('C:\\Users\Administrator\Desktop\爬虫\zhaopin\\new_taskcity01.xlsx')
sheet1 = data.sheet_by_name('Sheet1')
sheet2 = data.sheet_by_name('Sheet2')
sheet1_list = sheet1.col_values(1)
sheet2_list = sheet2.col_values(1)
pop_list = []
# 创建电子表格
workbook = openpyxl.Workbook()
worksheet = workbook.create_sheet(index=0)
for i in sheet1_list:
    if i not in sheet2_list:
        nrows = sheet1.nrows
        for r in range(nrows):
            if i in sheet1.row_values(r):
                print(sheet1.row_values(r))
                worksheet.append(sheet1.row_values(r))
        workbook.save('aaa.xlsx')