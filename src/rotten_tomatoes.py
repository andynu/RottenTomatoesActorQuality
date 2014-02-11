import json
import urllib

api_file = '.rottentomatoes_api_key'
api_key = open(api_file).read().rstrip()
service_url = 'http://api.rottentomatoes.com/api/public/v1.0'

def search(path,params):
  params['apikey'] = api_key
  url = service_url + path + '?' + urllib.urlencode(params)
  response = json.loads(urllib.urlopen(url).read())
  return response

def movie(name):
  return search('/movies.json', {'q': name, 'page_limit':'1'})
