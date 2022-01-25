import manipulate as mn
import os
print("import done")



filename = "/home/julian/Downloads/zuckerberg.mp4"
outfile = "out.mp4"
mn.manipulate_mp4(filename, outfile)
os.system("xdg-open "+outfile)
