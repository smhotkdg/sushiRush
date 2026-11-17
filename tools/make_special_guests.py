# 특별 손님 스프라이트: 기존 손님 그림 + 소품 합성 (4배로 그린 뒤 축소해 부드러운 외곽선)
import colorsys, math, sys
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
SRC='assets/restaurant/'; OUT=sys.argv[1] if len(sys.argv)>1 else 'assets/restaurant/'
import os; os.makedirs(OUT,exist_ok=True)
INK=(74,42,28,255); S=4
def layer(w,h): im=Image.new('RGBA',(w*S,h*S),(0,0,0,0)); return im, ImageDraw.Draw(im)
def down(im,w,h): return im.resize((w,h),Image.LANCZOS)
def P(*pts): return [(x*S,y*S) for x,y in pts]

def recolor(im, test, hue, sat_mul=1.0, light_add=0.0, region=None):
    im=im.copy(); px=im.load(); w,h=im.size
    for y in range(h):
        if region and not (region[1]<=y<region[3]): continue
        for x in range(w):
            if region and not (region[0]<=x<region[2]): continue
            r,g,b,a=px[x,y]
            if a==0 or not test(r,g,b): continue
            hh,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255)
            nr,ng,nb=colorsys.hls_to_rgb(hue/360,min(1,l+light_add),min(1,s*sat_mul))
            px[x,y]=(int(nr*255),int(ng*255),int(nb*255),a)
    return im
red=lambda r,g,b: r>120 and r>g*1.6 and r>b*1.5

def crown(cx,base,wd):           # 금왕관: 바닥 중심 (cx, base), 너비 wd
    im,d=layer(160,160); h=wd*0.62; x0=cx-wd/2
    pts=[(x0,base),(x0+wd*0.04,base-h*0.78),(x0+wd*0.26,base-h*0.40),(cx,base-h),(x0+wd*0.74,base-h*0.40),(x0+wd*0.96,base-h*0.78),(x0+wd,base)]
    d.polygon(P(*pts),fill=(246,190,64,255),outline=INK,width=int(2.2*S))
    d.rounded_rectangle([ (x0-1)*S,(base-h*0.22)*S,(x0+wd+1)*S,(base+h*0.12)*S ],radius=int(3*S),fill=(232,160,40,255),outline=INK,width=int(2.2*S))
    for px_,col in [(cx,(214,64,72,255)),(x0+wd*0.22,(70,150,210,255)),(x0+wd*0.78,(70,150,210,255))]:
        r=wd*0.07; d.ellipse([(px_-r)*S,(base-h*0.05-r)*S,(px_+r)*S,(base-h*0.05+r)*S],fill=col,outline=INK,width=int(1.2*S))
    for (tx,ty) in [(x0+wd*0.04,base-h*0.78),(cx,base-h),(x0+wd*0.96,base-h*0.78)]:
        r=wd*0.06; d.ellipse([(tx-r)*S,(ty-r)*S,(tx+r)*S,(ty+r)*S],fill=(255,236,150,255),outline=INK,width=int(1.2*S))
    d.line(P((x0+wd*0.12,base-h*0.55),(x0+wd*0.16,base-h*0.30)),fill=(255,240,190,230),width=int(1.6*S))
    return down(im,160,160)

def sparkle(img,pts):
    im,d=layer(160,160)
    for (x,y,r) in pts:
        star=[]; 
        for k in range(8):
            a=k*math.pi/4; rr_=r if k%2==0 else r*0.32; star.append((x+math.cos(a)*rr_,y+math.sin(a)*rr_))
        d.polygon(P(*star),fill=(255,214,90,255),outline=(176,116,20,255),width=int(0.8*S))
    img.alpha_composite(down(im,160,160)); return img

def necktie(cx,top,length):
    im,d=layer(160,160); w=length*0.44
    d.polygon(P((cx-w*0.42,top),(cx+w*0.42,top),(cx+w*0.22,top+length*0.18),(cx-w*0.22,top+length*0.18)),fill=(54,72,128,255),outline=INK,width=int(2*S))
    d.polygon(P((cx-w*0.22,top+length*0.16),(cx+w*0.22,top+length*0.16),(cx+w*0.5,top+length*0.86),(cx,top+length),(cx-w*0.5,top+length*0.86)),fill=(62,84,150,255),outline=INK,width=int(2*S))
    for k in range(3):
        y=top+length*(0.32+k*0.18); d.line(P((cx-w*0.32,y+3),(cx+w*0.32,y-3)),fill=(232,196,90,255),width=int(2*S))
    return down(im,160,160)

def sweat(x,y,r):
    im,d=layer(160,160)
    d.polygon(P((x,y-r*1.9),(x+r*0.95,y-r*0.1),(x-r*0.95,y-r*0.1)),fill=(140,206,246,255))
    d.ellipse([(x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S],fill=(140,206,246,255))
    d.line(P((x,y-r*1.9),(x+r*0.95,y-r*0.1)),fill=(52,110,170,255),width=int(1.6*S)); d.line(P((x,y-r*1.9),(x-r*0.95,y-r*0.1)),fill=(52,110,170,255),width=int(1.6*S))
    d.arc([(x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S],0,180,fill=(52,110,170,255),width=int(1.6*S))
    d.ellipse([(x-r*0.45)*S,(y-r*0.6)*S,(x-r*0.05)*S,(y-r*0.1)*S],fill=(255,255,255,220))
    return down(im,160,160)

def clock(x,y,r):
    im,d=layer(160,160)
    d.ellipse([(x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S],fill=(255,246,226,255),outline=INK,width=int(2*S))
    d.ellipse([(x-r*0.8)*S,(y-r*0.8)*S,(x+r*0.8)*S,(y+r*0.8)*S],outline=(214,90,64,255),width=int(1.6*S))
    d.line(P((x,y),(x,y-r*0.6)),fill=INK,width=int(2*S)); d.line(P((x,y),(x+r*0.45,y+r*0.15)),fill=INK,width=int(2*S))
    for a in (-0.55,0.55):
        bx,by=x+math.sin(a)*r*1.05,y-math.cos(a)*r*1.05; d.ellipse([(bx-r*0.28)*S,(by-r*0.28)*S,(bx+r*0.28)*S,(by+r*0.28)*S],fill=(214,90,64,255),outline=INK,width=int(1.2*S))
    return down(im,160,160)

def bandage(x,y,wd,ang,size=160):
    im,d=layer(size,size); h=wd*0.36
    c,s_=math.cos(ang),math.sin(ang)
    def rot(px_,py_): return (x+px_*c-py_*s_, y+px_*s_+py_*c)
    pts=[rot(-wd/2,-h/2),rot(wd/2,-h/2),rot(wd/2,h/2),rot(-wd/2,h/2)]
    d.polygon(P(*pts),fill=(246,214,170,255),outline=INK,width=int(1.6*S))
    pad=[rot(-wd*0.17,-h*0.42),rot(wd*0.17,-h*0.42),rot(wd*0.17,h*0.42),rot(-wd*0.17,h*0.42)]
    d.polygon(P(*pad),fill=(236,186,150,255))
    for k in (-1,1):
        for j in (-1,1):
            px_,py_=rot(k*wd*0.33,j*h*0.18); r=0.9; d.ellipse([(px_-r)*S,(py_-r)*S,(px_+r)*S,(py_+r)*S],fill=(196,140,100,255))
    return down(im,size,size)

def save(im,name): im.save(OUT+name+'.webp','WEBP',quality=92,method=6,lossless=False)

# ---------- VIP 미식가 (턱시도 고양이) ----------
VIP={'idle':(80,33,44),'blink':(80,33,44),'happy':(80,31,44),'angry':(82,33,44)}
for st,(cx,base,wd) in VIP.items():
    im=Image.open(SRC+f'tuxedo_{st}.webp').convert('RGBA')
    im=recolor(im,red,44,sat_mul=1.05,light_add=0.12,region=(30,92,140,140))   # 빨간 나비넥타이 → 금색
    im.alpha_composite(crown(cx,base,wd))
    if st in ('idle','happy'): im=sparkle(im,[(28,40,7),(138,96,5),(22,104,4)])
    save(im,'vip_'+st)

# ---------- 급한 직장인 (시바) ----------
RUSH={'idle':(80,112,44),'blink':(80,112,44),'happy':(80,110,44),'angry':(84,112,44)}
for st,(cx,top,ln) in RUSH.items():
    im=Image.open(SRC+f'shiba_{st}.webp').convert('RGBA')
    im.alpha_composite(necktie(cx,top,ln))
    if st!='happy': im.alpha_composite(sweat(30,58 if st!='angry' else 52,6))
    im.alpha_composite(clock(24,24,13))
    save(im,'rush_'+st)

# ---------- 길고양이 (삼색이 → 회갈색 길냥이) ----------
def stray(src,st,bx,by,ang):
    im=Image.open(SRC+src).convert('RGBA')
    rgb=im.convert('RGB'); a=im.getchannel('A')
    gray=ImageEnhance.Color(rgb).enhance(0.18)                 # 채도를 빼서 회색 톤
    tint=Image.new('RGB',im.size,(150,128,108))                 # 따뜻한 회갈색으로 살짝 물들임
    mixed=Image.blend(gray,Image.composite(tint,gray,Image.new('L',im.size,90)),0.35)
    out=Image.merge('RGBA',(*mixed.split(),a))
    out=recolor(out,lambda r,g,b: b>r*0.9 and r<140 and g<120,0,sat_mul=0.0)  # 보라 목줄 제거(회색)
    out.alpha_composite(bandage(bx,by,30,ang,192))
    save(out,'stray_'+st)
stray('calico_idle.webp','walk',100,40,-0.5)
stray('calico_happy.webp','eat',98,44,-0.4)
print('done', sorted(os.listdir(OUT)))
