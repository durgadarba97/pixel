#! /bin/bash
echo "displaying stream file $1"
sudo /home/spliff/rpi-rgb-led-matrix/utils/led-image-viewer --led-rows=64 --led-cols=64 --led-brightness=75 --led-gpio-mapping=adafruit-hat-pwm /home/spliff/PixelBoard/output/streams/$1.stream
exit 1