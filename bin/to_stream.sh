#! /bin/bash
echo "outputing script to stream file:$1"
sudo /home/spliff/rpi-rgb-led-matrix/utils/led-image-viewer --led-rows=64 --led-cols=64 --led-gpio-mapping=adafruit-hat-pwm /home/spliff/pixel/output/gifs/$1 -O/home/spliff/pixel/output/streams/$1.stream
exit 1