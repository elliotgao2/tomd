import tomd
import requests

r = requests.get('https://github.com/gaojiuli/toapi')
r.encoding = None
tomd.convert(r.text)

