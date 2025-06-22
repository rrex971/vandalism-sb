import random
import math
offset=0
def generate_particle(x, big=False):
    origin = x+random.randint(-40, 40)
    final = x+random.randint(-40, 40)
    if not big:
        val = random.randint(5,10)/10 # fade
        val2 = random.randint(10000,20000) # timing
        radian=random.random()*2
        scale=random.randint(10,20)/100
        for s in range(2):
            ease=0 if s==0 else 0
            offset = 0 if s==0 else 1
            colstr = "255,0,0" if s==1 else "0,255,255"
            print(f'''Sprite,Foreground,Centre,"sb\particle.png",{origin+offset},{offset}''')
            print(" P,0,0,,A")
            print(f" C,0,0,,{colstr}")
            print(f" S,0,0,,{scale}")
            print(" L,19806,60")
            print(f"  R,0,0,{val2},0,{radian}")
            print(f"  F,0,0,1000,0,{val}")
            print(f"  M,{ease},0,{val2},{origin+offset},{offset},{final+offset},{500+offset}")
            print(f"  F,0,{val2-1000},{val2},{val},0")
            print(" F,0,314239,,0")
    else:
        col=random.randint(150,200)
        col2=random.randint(col-20,col-10)
        scale=(random.randint(10,15)/100)*3
        radian=random.random()*2
        val = random.randint(3,8)/10
        val2 = random.randint(8000,13000)

        
        for s in range(2):
            ease=0 if s==0 else 0
            offset = 0 if s==0 else 1
            colstr = "255,0,0" if s==0 else "0,255,255"
            print(f'''Sprite,Foreground,Centre,"sb\particle_blur.png",{origin+offset},{offset}''')
            print(f" P,0,0,,A")
            print(f" C,0,0,,{colstr}")
            print(f" S,0,0,,{scale}")
            print(" L,19806,60")
            
            print(f"  R,0,0,{val2},0,{radian}")
            print(f"  F,0,0,1000,0,{val}")
            print(f"  M,{ease},0,{val2},{origin+offset},{offset},{final+offset},{500+offset}")
            print(f"  F,0,{val2-1000},{val2},{val},0")
            print(" F,0,314239,,0")
    print()
    
for i in range(-107, 747, 80):
    generate_particle(i, big=False)
for i in range(-107, 747, 160):
    generate_particle(i, big=True)