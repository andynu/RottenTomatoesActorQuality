import json
import urllib

api_key = open(".freebase_api_key").read()
service_url = 'https://www.googleapis.com/freebase/v1/search'

def search(params):
  params['key'] = api_key
  url = service_url + '?' + urllib.urlencode(params)
  response = json.loads(urllib.urlopen(url).read())
  return response['result']

if __name__ == '__main__':

  name = 'Steve Martin'
  print name

  actor_query = {'filter':'(all name:"'+name+'" type:/film/actor)'}
  actor = search(actor_query)[0] # hope it is the first hit.

  movies_query = {
    'filter':'(all type:/film/film contributor:"'+actor['name']+'")',
    'limit':'200'
    }
  
  for movie in search(movies_query):
    print '%(name)s (%(score)f)' % movie
