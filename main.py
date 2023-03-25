# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from selenium import webdriver
from ScanFage import searchMbasic
from base import BasePage
from face import FacebookPage
import re
import requests


keywords = ["FPT"]
stringCookie = 'datr=EmQIY52Yam-sdvWIu-8gQgV9; sb=zO8XYwJqnbt9730tnz9u-823; locale=vi_VN; c_user=100050499607227; xs=26%3ADcQ8Av7fQaOqxw%3A2%3A1679637998%3A-1%3A6383; presence=C%7B%22lm3%22%3A%22u.416683581703989%22%2C%22t3%22%3A%5B%7B%22i%22%3A%22u.101881715984442%22%7D%2C%7B%22i%22%3A%22u.416683581703989%22%7D%5D%2C%22utc3%22%3A1679638449633%2C%22v%22%3A1%7D; wd=1600x795; usida=eyJ2ZXIiOjEsImlkIjoiQXJzMGd5YzRpMGkzNSIsInRpbWUiOjE2Nzk2Mzg3ODB9; oo=v1'
token = 'EAAGNO4a7r2wBABrT7oPneyGyXe7TVjkqdUS5Tw3mWAKjrRCBTAhQfqGggznFNlFJRh6cHDCl5mrrBxEdFBUO7G8UwuYVZAgDtMZC89GTlOTjD6JDpayVRQCsyhyCEOagZBU1PEwNZCfHL90E3vi0cXj0TV6LkYhAdY9V6YJgCMFaVxfAQ0qDFrUvDbRudpAZD'
scan = searchMbasic()
scan.ScanFage(stringCookie,token,keywords,5,2,5,10)
