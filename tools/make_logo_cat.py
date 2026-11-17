"""로비 로고 애니메이션(logo_cat.webp): 삼색 고양이가 초밥을 먹으려는 6프레임 가로 시트.
기존 손님 그림(calico_*)과 초밥·접시 그림을 합성해 만든다. 프레임 크기 FW×FH."""
import math, sys
from PIL import Image, ImageDraw, ImageFilter
root=sys.argv[1] if len(sys.argv)>1 else 'assets/restaurant'
FW,FH=320,240
L=lambda n:Image.open(f'{root}/{n}.webp').convert('RGBA')
cat={k:L('calico_'+k).resize((192,192),Image.Resampling.LANCZOS) for k in ['idle','blink','happy']}
sushi=L('sushi_salmon').resize((128,128),Image.Resampling.LANCZOS).crop((5,20,123,107))
plate=L('ui_plate').resize((118,40),Image.LANCZOS)
def scaled(im,s): return im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
def put(fr,im,cx,cy,rot=0):
    if rot: im=im.rotate(rot,resample=Image.BICUBIC,expand=True)
    fr.alpha_composite(im,(round(cx-im.width/2),round(cy-im.height/2)))
def shadow(fr,cx,cy,w,h,a=70):
    sh=Image.new('RGBA',(FW,FH),(0,0,0,0)); ImageDraw.Draw(sh).ellipse((cx-w/2,cy-h/2,cx+w/2,cy+h/2),fill=(60,30,15,a))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
def marks(fr,x,y,s=1,col=(255,160,40,255)):            # 놀람 표시 세 줄
    d=ImageDraw.Draw(fr)
    for a,l in [(-60,16),(-25,20),(10,15)]:
        r=math.radians(a); x0,y0=x+math.cos(r)*8*s,y+math.sin(r)*8*s; x1,y1=x+math.cos(r)*(8+l)*s,y+math.sin(r)*(8+l)*s
        d.line((x0,y0,x1,y1),fill=(70,35,20,255),width=round(7*s)); d.line((x0,y0,x1,y1),fill=col,width=round(4*s))
def star(fr,cx,cy,r,col=(255,246,200,255),edge=(240,160,32,255)):
    d=ImageDraw.Draw(fr); pts=[]
    for k in range(8):
        a=k*math.pi/4; q=r if k%2==0 else r*0.3; pts.append((cx+math.cos(a)*q,cy+math.sin(a)*q))
    d.polygon(pts,fill=col,outline=edge)
def heart(fr,cx,cy,r,col=(255,110,140,255)):
    h=Image.new('RGBA',(FW,FH),(0,0,0,0)); d=ImageDraw.Draw(h)
    d.ellipse((cx-r,cy-r*0.8,cx,cy+r*0.2),fill=col); d.ellipse((cx,cy-r*0.8,cx+r,cy+r*0.2),fill=col)
    d.polygon([(cx-r*0.97,cy-r*0.1),(cx+r*0.97,cy-r*0.1),(cx,cy+r*1.05)],fill=col)
    fr.alpha_composite(h)
def bitten(im,bites):                                  # 왼쪽을 베어 문 초밥
    im=im.copy(); m=Image.new('L',im.size,255); d=ImageDraw.Draw(m)
    for bx,by,br in bites: d.ellipse((bx-br,by-br,bx+br,by+br),fill=0)
    a=im.split()[3]; from PIL import ImageChops; im.putalpha(ImageChops.multiply(a,m)); return im
def speed(fr,x,y,n=3,l=22):
    d=ImageDraw.Draw(fr)
    for k in range(n): d.line((x,y+k*10,x+l-k*4,y+k*10),fill=(255,255,255,220),width=4)

CS=0.98                                                 # 고양이 크기
cx0,cy0=118,128                                         # 고양이 중심
px,py=262,196                                           # 접시 중심
S=scaled(sushi,0.86)
frames=[]
def base(): fr=Image.new('RGBA',(FW,FH),(0,0,0,0)); shadow(fr,cx0,cy0+88,150,22); return fr
# 1 가만히: 초밥이 접시 위에서 반짝
fr=base(); shadow(fr,px,py+8,110,16,50); put(fr,plate,px,py); put(fr,S,px,py-26); put(fr,scaled(cat['idle'],CS),cx0,cy0); star(fr,px+40,py-58,9); frames.append(fr)
# 2 발견: 깜짝 + 초밥 쪽으로 몸이 살짝
fr=base(); shadow(fr,px,py+8,110,16,50); put(fr,plate,px,py); put(fr,S,px,py-28,-4); put(fr,scaled(cat['idle'],CS),cx0+6,cy0-4,-5); marks(fr,cx0+62,cy0-78); star(fr,px+44,py-62,11); star(fr,px-38,py-52,6); frames.append(fr)
# 3 두 손 번쩍: 초밥이 떠오른다
fr=base(); shadow(fr,px,py+8,110,16,50); put(fr,plate,px,py); put(fr,S,px-14,py-58,6); speed(fr,px+22,py-58); put(fr,scaled(cat['happy'],CS),cx0+12,cy0-8,-6); star(fr,px-50,py-96,8); frames.append(fr)
# 4 덥석: 초밥을 입 앞으로
fr=base(); shadow(fr,px,py+8,110,16,50); put(fr,plate,px,py); put(fr,scaled(cat['happy'],CS),cx0+22,cy0-10,-11); put(fr,scaled(S,0.84),cx0+62,cy0-30,18); frames.append(fr)
# 5 냠: 눈 감고 한 입, 밥알이 톡톡
fr=base(); shadow(fr,px,py+8,110,16,50); put(fr,plate,px,py); put(fr,scaled(cat['blink'],CS),cx0+16,cy0-4,-7)
put(fr,bitten(scaled(S,0.84),[(8,26,17),(12,44,14),(5,10,12)]),cx0+54,cy0-14,10)
d=ImageDraw.Draw(fr)
for (x,y,r) in [(cx0+28,cy0-40,5),(cx0+40,cy0-62,4),(cx0+92,cy0-50,4),(cx0+20,cy0-20,3)]: d.ellipse((x-r,y-r,x+r,y+r),fill=(255,255,255,255),outline=(200,170,140,255))
frames.append(fr)
# 6 행복: 빈 접시, 하트
fr=base(); shadow(fr,px,py+8,110,16,50); put(fr,plate,px,py); put(fr,scaled(cat['blink'],CS),cx0,cy0)
heart(fr,cx0+70,cy0-84,13); heart(fr,cx0+96,cy0-110,9,(255,150,175,255)); star(fr,cx0-74,cy0-70,8); frames.append(fr)

sheet=Image.new('RGBA',(FW*len(frames),FH),(0,0,0,0))
for i,f in enumerate(frames): sheet.alpha_composite(f,(i*FW,0))
sheet.save(f'{root}/logo_cat.webp','WEBP',quality=90,method=6)
print('ok',sheet.size)
