
import os
import re

countries = {}
ip_ranges = ""
country_names = {}

def query(ip, raiseError=False):
  global countries, country_names, ip_ranges
  if not ip_ranges:
    setup()
  try:
    parts = ip.split(".")
    find = "%c%c%c" % (int(parts[0]), int(parts[1]), int(parts[2]))
  except:
    # IPv6 is not supported
    return (None, None)
  lo = 0
  hi = (len(ip_ranges)) / 4   
  while lo < hi:
    mid = (lo+hi) // 2
    midval = ip_ranges[mid * 4:mid * 4 + 3]
    if midval < find:
      lo = mid + 1
    elif midval > find: 
      hi = mid
    else:
      break
  found = hi * 4 - 4
  if ip_ranges[found:found + 3] > find:
    found -= 4
  id = ord(ip_ranges[found + 3:found + 4])
  return (countries.get(id), country_names.get(id))

def setup():
  global countries, country_names, ip_ranges
  data = open(os.path.join(os.path.dirname(__file__),
                           "geoip.bin"), "rb").read()
  country_data = data[:data.find("\n")]
  pattern = re.compile("(\d+)\:([^\|]+)\|")
  for country in pattern.findall(country_data):
    countries[int(country[0])] = country[1]
  data = data[data.find("\n") + 1:]
  country_names_data = data[:data.find("\n")]
  for name in pattern.findall(country_names_data):
    country_names[int(name[0])] = name[1]
  ip_ranges = data[data.find("\n") + 1:]
 
