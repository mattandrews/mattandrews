#!/bin/sh
JEKYLL_ENV=production jekyll build
rsync -avr --rsh='ssh -p25000' --delete-after --delete-excluded _site/ matt@162.243.234.162:/var/www/mattandrews/matt