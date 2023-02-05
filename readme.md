# Intro

Interested in human interface and control
Type of person who likes physical radio dials
The sonos app is lacking, laggy, slow, flakey

My use case for sonos is:
choose one of three groups of speakers
Living Room + Kitchen
Bedroom
All
select media
 fixed playlist
 latest episode of podcast

play/pause
next/prev
volume (group/individual

I figured this could be done with a single rotary encoder (scroll + click) and a back button.

## Rotary Encoder

Rotary Encoder
https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-use-a-rotary-encoder-with-the-raspberry-pi


## Sonos

This was made spectacularly easy with the soco python library, I started off using the sonos-cli and subprocess.run to invoke, but the latency was noticable and was not going to work with volume changes. 

Soco
https://docs.python-soco.com/en/latest/examples.html#getting-all-your-devices


## Podcasts

Greg made downloading the latest episode of everything really easy

greg
https://github.com/manolomartinez/greg

## Hardware
Beware - you can lose hours browsing ali express looking at the amazing variety of parts available.

I bought a bunch of random things:

Rotary Encoders

Buttons

Retropie hat
https://www.aliexpress.com/item/32970035492.html?srcSns=sns_Copy&spreadType=socialShare&bizType=ProductDetail&social_params=20535536761&aff_fcid=57c56b98972d4969830f68948b8fdf38-1650812153826-09189-_mKCXEJy&tt=MG&aff_fsk=_mKCXEJy&aff_platform=default&sk=_mKCXEJy&aff_trace_key=57c56b98972d4969830f68948b8fdf38-1650812153826-09189-_mKCXEJy&shareId=20535536761&businessType=ProductDetail&platform=AE&terminal_id=6217f8c4c44c41dc8ee30f6d1e8f66bf&afSmartRedirect=y


## Reference

Pi Pinout
https://www.etechnophiles.com/raspberry-pi-zero-gpio-pinout-specifications-programming-language/

ST7789 Resources
https://github.com/pimoroni/st7789-python
https://techatronic.com/st7789-raspberry-pi/



Simple KV
https://pythonhosted.org/simplekv/




