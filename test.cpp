/*
 * newtest.c
 *
 * Copyright (c) 2014 Jeremy Garff <jer @ jers.net>
 *
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification, are permitted
 * provided that the following conditions are met:
 *
 *     1.  Redistributions of source code must retain the above copyright notice, this list of
 *         conditions and the following disclaimer.
 *     2.  Redistributions in binary form must reproduce the above copyright notice, this list
 *         of conditions and the following disclaimer in the documentation and/or other materials
 *         provided with the distribution.
 *     3.  Neither the name of the owner nor the names of its contributors may be used to endorse
 *         or promote products derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
 * FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
 * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
 * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */


//static char VERSION[] = "XX.YY.ZZ";

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <signal.h>
#include <stdarg.h>
#include <getopt.h>

#include <iostream>
#include <fstream>
#include <sstream>

#include <vector>
#include <iomanip>
#include <cstdint>

#include <ws2811/clk.h>
#include <ws2811/gpio.h>
#include <ws2811/dma.h>
#include <ws2811/pwm.h>
//#include "rpi_ws281x/version.h"

#include <ws2811/ws2811.h>


#define ARRAY_SIZE(stuff)       (sizeof(stuff) / sizeof(stuff[0]))

// defaults for cmdline options
#define TARGET_FREQ             WS2811_TARGET_FREQ
#define GPIO_PIN                18
#define DMA                     10
//#define STRIP_TYPE            WS2811_STRIP_RGB		// WS2812/SK6812RGB integrated chip+leds
#define STRIP_TYPE              WS2811_STRIP_GBR		// WS2812/SK6812RGB integrated chip+leds
//#define STRIP_TYPE            SK6812_STRIP_RGBW		// SK6812RGBW (NOT SK6812RGB)

//#define WIDTH                   8
//#define HEIGHT                  8
#define LED_COUNT              34

#define ACTUALLY_RUN_IT false

//int width = WIDTH;
//int height = HEIGHT;
int led_count = LED_COUNT;

ws2811_t ledstring;

int clear_on_exit = 0;

ws2811_led_t *matrix;

static uint8_t running = 1;

void matrix_render(void)
{
    int x;

    for (x = 0; x < led_count; x++)
    {
            ledstring.channel[0].leds[x] = matrix[x];
    }
}

void matrix_clear(void)
{
    int x;

    for (x = 0; x < led_count; x++)
        {
            matrix[x] = 0;
        }

}

int dotspos[] = { 0, 1, 2, 3, 4, 5, 6, 7 };
ws2811_led_t dotcolors[] =
{
    0x00200000,  // red
    0x00201000,  // orange
    0x00202000,  // yellow
    0x00002000,  // green
    0x00002020,  // lightblue
    0x00000020,  // blue
    0x00100010,  // purple
    0x00200010,  // pink
};

ws2811_led_t dotcolors_rgbw[] =
{
    0x00200000,  // red
    0x10200000,  // red + W
    0x00002000,  // green
    0x10002000,  // green + W
    0x00000020,  // blue
    0x10000020,  // blue + W
    0x00101010,  // white
    0x10101010,  // white + W

};

void matrix_bottom(void)
{
    int i;

    for (i = 0; i < (int)(ARRAY_SIZE(dotspos)); i++)
    {
        dotspos[i]++;
        if (dotspos[i] > (led_count - 1))
        {
            dotspos[i] = 0;
        }

        if (ledstring.channel[0].strip_type == SK6812_STRIP_RGBW) {
            matrix[dotspos[i] ] = dotcolors_rgbw[i];
        } else {
            matrix[dotspos[i] ] = dotcolors[i];
        }

    }
}

static void ctrl_c_handler(int signum)
{
	(void)(signum);
    running = 0;
}

static void setup_handlers(void)
{
    struct sigaction sa;

    sa.sa_handler = ctrl_c_handler;

    sigaction(SIGINT, &sa, NULL);
    sigaction(SIGTERM, &sa, NULL);
}


void parseargs(int argc, char **argv, ws2811_t *ws2811)
{
	int index;
	int c;

	static struct option longopts[] =
	{
		{"help", no_argument, 0, 'h'},
		{"dma", required_argument, 0, 'd'},
		{"gpio", required_argument, 0, 'g'},
		{"invert", no_argument, 0, 'i'},
		{"clear", no_argument, 0, 'c'},
		{"strip", required_argument, 0, 's'},
		{"height", required_argument, 0, 'y'},
		{"width", required_argument, 0, 'x'},
		{"version", no_argument, 0, 'v'},
		{0, 0, 0, 0}
	};

	while (1)
	{

		index = 0;
		c = getopt_long(argc, argv, "cd:g:his:vx:y:", longopts, &index);

		if (c == -1)
			break;

		switch (c)
		{
		case 0:
			/* handle flag options (array's 3rd field non-0) */
			break;

		case 'h':
			//fprintf(stderr, "%s version %s\n", argv[0], "0");
			fprintf(stderr, "Usage: %s \n"
				"-h (--help)    - this information\n"
				"-s (--strip)   - strip type - rgb, grb, gbr, rgbw\n"
				"-x (--width)   - matrix width (default 8)\n"
				"-y (--height)  - matrix height (default 8)\n"
				"-d (--dma)     - dma channel to use (default 10)\n"
				"-g (--gpio)    - GPIO to use\n"
				"                 If omitted, default is 18 (PWM0)\n"
				"-i (--invert)  - invert pin output (pulse LOW)\n"
				"-c (--clear)   - clear matrix on exit.\n"
				"-v (--version) - version information\n"
				, argv[0]);
			exit(-1);

		case 'D':
			break;

		case 'g':
			if (optarg) {
				int gpio = atoi(optarg);
/*
	PWM0, which can be set to use GPIOs 12, 18, 40, and 52.
	Only 12 (pin 32) and 18 (pin 12) are available on the B+/2B/3B
	PWM1 which can be set to use GPIOs 13, 19, 41, 45 and 53.
	Only 13 is available on the B+/2B/PiZero/3B, on pin 33
	PCM_DOUT, which can be set to use GPIOs 21 and 31.
	Only 21 is available on the B+/2B/PiZero/3B, on pin 40.
	SPI0-MOSI is available on GPIOs 10 and 38.
	Only GPIO 10 is available on all models.

	The library checks if the specified gpio is available
	on the specific model (from model B rev 1 till 3B)

*/
				ws2811->channel[0].gpionum = gpio;
			}
			break;

		case 'i':
			ws2811->channel[0].invert=1;
			break;

		case 'c':
			clear_on_exit=1;
			break;

		case 'd':
			if (optarg) {
				int dma = atoi(optarg);
				if (dma < 14) {
					ws2811->dmanum = dma;
				} else {
					printf ("invalid dma %d\n", dma);
					exit (-1);
				}
			}
			break;

		case 's':
			if (optarg) {
				if (!strncasecmp("rgb", optarg, 4)) {
					ws2811->channel[0].strip_type = WS2811_STRIP_RGB;
				}
				else if (!strncasecmp("rbg", optarg, 4)) {
					ws2811->channel[0].strip_type = WS2811_STRIP_RBG;
				}
				else if (!strncasecmp("grb", optarg, 4)) {
					ws2811->channel[0].strip_type = WS2811_STRIP_GRB;
				}
				else if (!strncasecmp("gbr", optarg, 4)) {
					ws2811->channel[0].strip_type = WS2811_STRIP_GBR;
				}
				else if (!strncasecmp("brg", optarg, 4)) {
					ws2811->channel[0].strip_type = WS2811_STRIP_BRG;
				}
				else if (!strncasecmp("bgr", optarg, 4)) {
					ws2811->channel[0].strip_type = WS2811_STRIP_BGR;
				}
				else if (!strncasecmp("rgbw", optarg, 4)) {
					ws2811->channel[0].strip_type = SK6812_STRIP_RGBW;
				}
				else if (!strncasecmp("grbw", optarg, 4)) {
					ws2811->channel[0].strip_type = SK6812_STRIP_GRBW;
				}
				else {
					printf ("invalid strip %s\n", optarg);
					exit (-1);
				}
			}
			break;

		case 'v':
			//fprintf(stderr, "%s version %s\n", argv[0], "0");
			exit(-1);

		case '?':
			/* getopt_long already reported error? */
			exit(-1);

		default:
			exit(-1);
		}
	}
}

int mat_read(std::vector<std::vector<ws2811_led_t>> *array )
{
	std::string line;                    /* string to hold each line */
 	std::string filename = "led.csv";

	std::ifstream f (filename);   /* open file */
	if (!f.is_open()) {     /* validate file open for reading */
		std::perror (("error while opening file" + filename).c_str());
	        return -1;
	}

	while (std::getline (f, line))
  {
		std::string val;
		std::vector<ws2811_led_t> row;
		std::stringstream s (line);
	        while (std::getline (s, val, ','))
                {
                  ws2811_led_t item = (ws2811_led_t)std::strtoul(val.c_str(), NULL, 0);
            		  row.push_back (item);
                }

        	array->push_back (row);
  }
  std::cout << "number of frames read from csv:" << array->size() <<"\n";
    	f.close();

  return  array->size();
}


void update_frame(int frame, ws2811_led_t* matrix, std::vector<std::vector<ws2811_led_t>>* array)
{
  std::cout << "hello";
  std::vector<ws2811_led_t> & row = array->at(frame);
  for (int x = 0; x < led_count; x++)
      {
          matrix[x] = row.at(x);
      }

  std::cout << "ok";

}

void matrix_render2()
{
  int x;
  for (x = 0; x < led_count; x++)
      {
          std::cout << std::setfill('0') << std::setw(8) << std::hex << matrix[x] << "  ";
      }
}


int main(int argc, char *argv[])
{
      matrix = new ws2811_led_t[34];


      std::vector<std::vector<ws2811_led_t>> array; /// we are going to load our csv array. lines is number of leds, columns is the number of frames
      int num_frames = mat_read(&array);
      // Displays the csv we just read. not really necessary, make it a debug feature

      std::cout << "complete array\n\n";
      for (auto& row : array)
        {           /* iterate over rows */
          for (auto& val : row)        /* iterate over vals */
                {
  	               std::cout << std::setfill('0') << std::setw(8) << std::hex << val << "  ";
                }
          std::cout << "\n";
        }
        std::cout << "me?ok\n";

    ws2811_channel_t channel0;
    channel0.gpionum = GPIO_PIN;
    channel0.count 		= LED_COUNT;
    channel0.invert 		= 0;
    channel0.brightness = 255;
    channel0.strip_type = STRIP_TYPE;

std::cout << "got this far\n";
    ws2811_channel_t channel1;
    channel1.gpionum    = 0;
    channel1.count      = 0;
    channel1.invert     = 0;
    channel1.brightness = 0;

std::cout << "got here\n";
    ledstring.freq    = TARGET_FREQ;
    ledstring.dmanum  = DMA;
    ledstring.channel[0] = channel0;
    ledstring.channel[1] = channel1;

    ws2811_return_t ret;

    std::cout << "did this bit\n";

    parseargs(argc, argv, &ledstring);



    std::cout << "parseargs ok\n";

    //size_t zz = sizeof(ws2811_led_t) * led_count;

    //matrix = (ws2811_led_t*) malloc(zz+1); //really?

    //matrix = new ws2811_led_t[led_count*20];

    if (ACTUALLY_RUN_IT)
    {
      setup_handlers();

      std::cout << "setup handlers ok";

      if ((ret = ws2811_init(&ledstring)) != WS2811_SUCCESS)
      {
          fprintf(stderr, "ws2811_init failed: %s\n", ws2811_get_return_t_str(ret));
          return ret;
      }
    }

    int frame = 0;

    while (running)
    {
        std::cout << "what about this?\n";
        //    	matrix_bottom(); // this is the old method to updamatrix_render();te the matrix colours, I will use the new one that loads from a csv
	      update_frame(frame % num_frames ,matrix,&array);
        std::cout << "update_frame ok\n";
        //matrix_render();
        matrix_render2();
        std::cout << "matrix_render2 ok\n";

        if (ACTUALLY_RUN_IT && (ret = ws2811_render(&ledstring)) != WS2811_SUCCESS)
        {
            fprintf(stderr, "ws2811_render failed: %s\n", ws2811_get_return_t_str(ret));
            break;
        }

        // 15 frames /sec
        usleep(1000000 / 15);
        frame++;
    }

    if (clear_on_exit) {
	matrix_clear();
	matrix_render();
	ws2811_render(&ledstring);
    }

    ws2811_fini(&ledstring);

    printf ("\n");
    return ret;
}
