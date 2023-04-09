
from PIL import Image
from time import time, sleep
from math import floor
from os import system,rmdir,mkdir,listdir
from os.path import isdir
from sys import argv

def bin2dec(binary):
 
    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal
 

if len(argv) != 3:
    print("usage: convert_video.py [invideo.webm] [outputfile.bin]")
    quit(-1)

start_tick = time()
filename = argv[1]
output = argv[2]

'''
if isdir("./temp/"):
    rmdir("./temp/")

mkdir("./temp/")

print("Splitting frames... (this might take a bit)")
response_code = system(f"ffmpeg -i {filename} ./temp/frame_%04d.png")
if response_code != 0:
    print("Something went wrong in ffmpeg. Exitting.")
    quit(-1)
'''
frame_count = len(listdir("./temp/"))
print(f"Frames split successfully! ({frame_count} frames)")

print("Parsing data...")
bin_file = open(output,"x")
bits = ["0","0","0","0","0","0","0","0"]
bit_cursor = 0
bytes_written = 0
sorted = listdir("./temp/")
sorted.sort()
for i in sorted:
    bytes_written = 0
    print(f"Frame {i}/{frame_count}")
    img = Image.open(f"./temp/{i}")
    img.resize([160,128])
    for iy in range(img.size[1]):
        for ix in range(img.size[0]):
            coord = x,y = ix,iy
            pixel = img.getpixel(coord)
            bits[bit_cursor] = (pixel[0] > 50 and "1") or "0"
            if bit_cursor >= 7:
                string = bin2dec(int("".join(bits)))
                bin_file.write(chr(string))
                bin_file.flush()
                bit_cursor = 0
                bytes_written = bytes_written + 1
            else:
                bit_cursor = bit_cursor + 1

    string = bin2dec(int("".join(bits)))
    bin_file.write(chr(string))
    bin_file.flush()
    bit_cursor = 0
    bytes_written = bytes_written + 1
    img.close()
    print(f"Bytes written: {bytes_written}")

bin_file.close()
print(f"Finished in {floor(time() - start_tick)} seconds.")