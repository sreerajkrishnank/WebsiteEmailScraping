f = open ("out.txt")
out_f = open ("outf.txt", 'w')
while True:
    c = f.read(1)
    if not c:
      break
    if c != '\n':
        out_f.write(c)
        out_f.flush()
    elif c == '\n' and f.read(1) == 'h':
        out_f.write(c + 'h')
        out_f.flush()
    else:
        continue