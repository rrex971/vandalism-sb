import random

def generate_particle(x, big=False):
    origin = x+random.randint(-100, 100)
    final = x+random.randint(-100, 100)
    if not big:
        col=random.randint(200,255)
        colstr = f"{col},{col},{col}"
        print(f'''Sprite,Foreground,Centre,"sb\particle.png",{origin},0''')
        print(f" C,0,0,,{colstr}")
        print(f" S,0,0,,{random.randint(10,15)/100}")
        print(" L,19806,75")
        val = random.randint(5,10)/10
        val2 = random.randint(10000,20000)
        print(f"  F,0,0,1000,0,{val}")
        print(f"  M,0,0,{val2},{origin},0,{final},500")
        print(f"  F,0,{val2-1000},{val2},{val},0")
        print(" F,0,314239,,0")
    else:
        col=random.randint(150,200)
        colstr = f"{col},{col},{col}"
        print(f'''Sprite,Foreground,Centre,"sb\particle_blur.png",{origin},0''')
        print(f" C,0,0,,{colstr}")
        print(f" S,0,0,,{(random.randint(10,15)/100)*3}")
        print(" L,19806,60")
        val = random.randint(3,8)/10
        val2 = random.randint(8000,13000)
        print(f"  F,0,0,1000,0,{val}")
        print(f"  M,0,0,{val2},{origin},0,{final},500")
        print(f"  F,0,{val2-1000},{val2},{val},0")
        print(" F,0,314239,,0")
    print()
    
for i in range(0, 640, 80):
    generate_particle(i, big=False)
for i in range(0, 640, 160):
    generate_particle(i, big=True)