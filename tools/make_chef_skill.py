"""규리 필살기 포즈(gyuri_skill.webp): 손질 중인 규리 + 불꽃 오라 + 반짝임. 기존 그림을 합성해 만든다."""
import math, random, sys
from PIL import Image, ImageFilter, ImageDraw, ImageChops
root=sys.argv[1] if len(sys.argv)>1 else 'assets/restaurant'
random.seed(7)
src=Image.open(f'{root}/gyuri_cook.webp').convert('RGBA')
S=src.width; pad=0
alpha=src.split()[3]
def glow(a,grow,blur,color,op):
    m=a
    for _ in range(grow): m=m.filter(ImageFilter.MaxFilter(5))
    m=m.filter(ImageFilter.GaussianBlur(blur)).point(lambda v:int(v*op))
    layer=Image.new('RGBA',src.size,color); layer.putalpha(m); return layer
out=Image.new('RGBA',src.size,(0,0,0,0))
# 불꽃: 바깥 주황, 안쪽 노랑. 위쪽으로 넘실대는 혀 모양을 더한다.
flame=Image.new('L',src.size,0); d=ImageDraw.Draw(flame)
for i in range(11):
    x=S*0.12+i*S*0.076+random.uniform(-4,4); h=S*random.uniform(0.18,0.32); w=S*0.07
    base=S*0.30+abs(i-5)*S*0.035
    d.polygon([(x-w,base+h*0.6),(x+random.uniform(-6,6),base-h*0.55),(x+w,base+h*0.6)],fill=255)
flame=ImageChops.lighter(flame,alpha.filter(ImageFilter.MaxFilter(9)))
aura=Image.new('RGBA',src.size,(0,0,0,0))
aura.alpha_composite(glow(flame,3,6,(255,120,40,255),0.8))
aura.alpha_composite(glow(flame,1,3,(255,196,60,255),0.85))
fade=Image.linear_gradient('L').resize(src.size).point(lambda v:255 if v<150 else int(255*(255-v)/105))
aura.putalpha(ImageChops.multiply(aura.split()[3],fade))
out.alpha_composite(aura)
out.alpha_composite(glow(alpha,2,3,(255,246,190,255),1.0))
out.alpha_composite(src)
# 반짝임 별
d=ImageDraw.Draw(out)
def star(cx,cy,r,col):
    pts=[]
    for k in range(8):
        a=k*math.pi/4; q=r if k%2==0 else r*0.32
        pts.append((cx+math.cos(a)*q,cy+math.sin(a)*q))
    d.polygon(pts,fill=col)
for cx,cy,r in [(S*0.13,S*0.30,11),(S*0.88,S*0.24,13),(S*0.84,S*0.62,8),(S*0.10,S*0.66,8)]:
    star(cx,cy,r+2,(255,160,40,255)); star(cx,cy,r,(255,250,215,255))
out.save(f'{root}/gyuri_skill.webp','WEBP',quality=92)
print('ok',out.size)
