import json
import urllib

api_file = '/home/andy/RottenTomatoesActorQuality/.freebase_api_key'
api_key = open(api_file).read()
service_url = 'https://www.googleapis.com/freebase/v1/search'

def search(params):
  params['key'] = api_key
  url = service_url + '?' + urllib.urlencode(params)
  response = json.loads(urllib.urlopen(url).read())
  result = response['result']
  return result

def actor(name):
  return search({
    'filter':'(all name:"'+name+'" type:/film/actor)'
  })[0] # hope it is the first hit.

def all_actors():
  return search({
    'filter':'(all type:/film/actor)',
    'limit':'200'
  })

def movies(actor_name):
  return search({
    'filter':'(all type:/film/film contributor:"'+actor_name+'")',
    'limit':'200'
  })

if __name__ == '__main__':
  for actor in all_actors():
    print
    print actor['name']
    for movie in movies(actor['name']):
      print movie['name']

