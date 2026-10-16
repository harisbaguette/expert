import sys
from PIL import Image
# 쓰는 법: python3 잘못-그림-합치기.py <앞 판 png> <잘못-그림-카드-찍기.cjs가 만든 c0@2x~c3@2x.png 폴더> <내보낼 png>
src,gen,out=sys.argv[1:4]
im=Image.open(src).convert('RGB'); W,H=im.size
BG=(254,254,254); LINE=(212,240,254)
rows=[(0,213),(217,397),(401,577),(581,761),(765,943),(947,1136),(1140,1402)]
def content(img,box):
    c=img.crop(box); m=c.convert('L').point(lambda v:255 if v<235 else 0); b=m.getbbox()
    return c.crop(b),(box[0]+b[0])
old=[]
for a,b in rows:
    for x0,x1 in ((0,557),(564,1122)):
        c,x=content(im,(x0,a,x1,b)); old.append((c,x-x0))
new=[]
for i in range(4):
    c=Image.open(gen+f'/c{i}@2x.png').convert('RGB'); c=c.resize((c.width//2,c.height//2),Image.LANCZOS)
    cc,x=content(c,(0,0,c.width,c.height)); new.append((cc,x))
o=old
# 앞 판 칸 번호: 0질문 1대상 2종류 3권한 4시점 5사실 6기준 7누락 8관계 9조건 10근거없는 11확인추정 12보고 13목적
cards=o[0:4]+['A']+o[4:10]+['B']+o[10:12]+['C']+o[12:13]+['D']+o[13:14]
nm={'A':0,'B':1,'C':2,'D':3}
assert len(cards)==18
pitch=184; top=217; NR=9
outH=top+pitch*(NR-1)-4+72
cv=Image.new('RGB',(W,outH),BG)
hl=im.crop((0,213,W,217))
for r in range(NR):
    if r==0: a,b=0,213
    else: a=top+pitch*(r-1); b=a+180
    if r<NR-1: cv.paste(hl,(0,b))
    va=(55 if r==0 else a+8); vb=b-8
    for y in range(va,vb):
        for x in range(559,563): cv.putpixel((x,y),LINE)
    for col in (0,1):
        it=cards[r*2+col]
        if isinstance(it,str):
            c,xo=new[nm[it]]; x=(0 if col==0 else 564)+xo
        else:
            c,xr=it; x=(0 if col==0 else 564)+xr
        cy=(59+193)//2 if r==0 else (a+b)//2
        cv.paste(c,(x,cy-c.height//2))
cv.save(out); print(cv.size)
