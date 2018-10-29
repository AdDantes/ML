from PIL import Image

im  = Image.open('D:\project\datawj\\bb.jpg')#读取图片
#保存图片
# im.save('weixin1.bmp')
#获取图片宽高D
# print(im.size)

width =im.size[0]#图片宽度
hight = im.size[1]#图片高度

#获取像素颜色
# print(im.getpixel((1,19)))

fh = open('2.txt','a')
for i in range(0,width):
    for j in range(0,hight):
        cl = im.getpixel((i,j))
        print(cl)
        # if cl ==0:
        #     fh.write('1')
        # else:
        #     fh.write('0')