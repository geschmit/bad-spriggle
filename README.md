# bad-spriggle
Bad Apple ported to the Sprig portable handheld(Raspberry Pi Pico H). You know it had to be done.


## The task
### What are we going for?
We need to cram ["Bad Apple!!"](https://www.youtube.com/watch?v=FtutLA63Cp8), a 3:40 music video into a <1 MB disk space. This will require a LOT of compression, workarounds, and hopefully not a super large headache to figure out.

The goal:
- Fit in under, if not exactly at 1 MB
- Run at >=30 FPS


### How did we do it?
Running through the list here...
```
Sprig's display size(ST7735R) ................... 160x128 px
Bad Apple's length .............................. 3:30 (approx. 210 sec.)
The original video's size ....................... 5305712 bytes
Bytes per frame, using split bits(on sprig) ..... 81 bytes
Bytes/Second, using bit method .................. 2430 b/s
Total size of uncompressed pixel data ........... 510300 bytes
Compressed data ................................. 
```

## Running
This requires a Sprig. I will not be providing instructions for standalone Pico installs, as it requires all the built-in parts that the sprig has.

### Before starting
Ensure CircuitPython 8.X is installed on your Sprig. Make sure it's the Pico version and not the Sprig or Pico W version.
All libraries needed should be included in a recent release.

### Copying
- Copy the files to your `CIRCUITPY` drive.
- By default, this should run fine. If any issues appear, check the serial console and open a issue.


## Licensing
Licensed under GNU GPL v3.0.
