from PIL import Image, ImageFilter
S='/tmp/claude-0/-home-claude/23972080-ba8e-5850-81e6-f070dcea3db4/scratchpad/'
bg=Image.open(S+'art/table.png').convert('RGBA')
names=['veneer-sycamore','veneer-birch','veneer-oak','veneer-cherry','veneer-cedar','veneer-wenge']
PX,PY=600,900          # точка схождения веера (ниже кадра)
CW,CH=260,720
for i,n in enumerate(names):
    ang=35-i*14
    sw=Image.open('/home/claude/marketri-site/img/'+n+'.jpg').convert('RGBA').resize((CW-4,CH-4))
    card=Image.new('RGBA',(CW,CH),(36,23,15,255)); card.paste(sw,(2,2))
    sh=Image.new('RGBA',(CW,CH),(8,4,2,160))
    def put(img, dy=0, blur=0):
        L=Image.new('RGBA',(1600,1600),(0,0,0,0))
        L.paste(img,(800-CW//2,800-CH+40))          # низ карточки у центра поворота
        L=L.rotate(ang,resample=Image.BICUBIC,center=(800,800))
        if blur: L=L.filter(ImageFilter.GaussianBlur(blur))
        bg.alpha_composite(L,(PX-800,PY-800+dy))
    put(sh,16,14); put(card)
bg.convert('RGB').save(S+'art/species.png'); print('ok')
