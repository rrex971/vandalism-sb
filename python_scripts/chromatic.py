k=False
k2=False
first=True
loopc1 = "  S,0,0,309,0.21,0.2\n"
loopc2 = "  S,0,0,309,0.215,0.2\n"
with open("mappers.txt") as f1:
    with open("CA_out.txt", "w") as f2:
        for i in f1.readlines():
            if i.startswith("Sprite"):
                if not first:
                    ts = lines[index2]
                    lines[index2] = f" P,0,{ts},,A\n C,0,{ts},,255,0,0\n"
                    lines[index]= loopc1
                    f2.writelines(lines)
                    lines[index2] = f" P,0,{ts},,A\n C,0,{ts},,0,255,255\n"
                    lines[index]= loopc2
                    f2.writelines(lines)
                first=False
                lines=[]
                index=-1
                index2=-1
                k=True
                
            
            if k2:
                ts = i.split(",")[1].strip()
                index2=len(lines)
                lines.append(ts)
                k=False
                k2=False
            if k:
                k2=True
                
            if i.startswith(" L"):
                index=len(lines)+1
            lines.append(i)
        ts = lines[index2]
        lines[index2] = f" P,0,{ts},,A\n C,0,{ts},,255,0,0\n"
        lines[index]= loopc1
        f2.writelines(lines)
        lines[index2] = f" P,0,{ts},,A\n C,0,{ts},,0,255,255\n"
        lines[index]= loopc2
        f2.writelines(lines)
        