#! /bin/bash
echo "outputing script to stream file:$2"
sudo /home/spliff/rpi-rgb-led-matrix/utils/led-image-viewer --led-rows=64 --led-cols=64 --led-gpio-mapping=adafruit-hat-pwm /home/spliff/PixelBoard/output/gifs/$1 -O/home/spliff/PixelBoard/output/streams/$2.stream
exit 1