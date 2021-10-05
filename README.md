# led_brain

Currently there is a tk GUI interface for coloring neopixels, with no driver. 

This is far from ideal, but it is how I thought about solving it. I am breaking the problem into 2 parts. 

First there is a remapping from 3D sequential data into a serialized line, this is done for every frame and a pseudo image is formed. Then each line is outputted from this image to the led strip. 

Each line on the png represents the whole sequence of the LED strip. Lines will be read in sequence. 

## TODO:

- add driver so that it actually drives the leds
- add thread to read png in a loop and write it to leds
- synchronize that thread with the gui
- Add main bit which will generate pngs from sequential 3D data

## C version

I've installed the `rpi_ws281x` shared library by compiling it with the options:

     cmake -D BUILD_SHARED=ON ..
     make
     sudo make install

Then I changed the references to use the installed version in the test.c

As `"clk.h"` -> `<ws2811/clk.h>`

Removed references to version so I could remove version.h then I compiled with:

    g++ -std=c++0x test.cpp -lws2811

* note that libws2811.so becomes l (instead of lib) and it loses the .so part as well

To run it you need sudo and `-c` to clear when ending so:

    sudo bin/main -c

