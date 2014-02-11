from apiclient import APIClient, RateLimiter

class FreebaseAPI(APIClient):
  API_FILE = '.freebase_api_key'
  API_KEY = open(API_FILE).read()
  BASE_URL = 'https://www.googleapis.com/freebase/v1/'

  def search(self,params):
    params['apikey'] = self.API_KEY
    path = 'search'
    return self.call(path, **params)['result']

  def actor(self,name):
    return self.search({
      'filter':'(all name:"'+name+'" type:/film/actor)'
    })[0] # hope it is the first hit.

  def all_actors(self):
    return self.search({
      'filter':'(all type:/film/actor)',
      'limit':'200'
    })

  def movies(self,actor_name):
    return self.search({
      'filter':'(all type:/film/film contributor:"'+actor_name+'")',
      'limit':'200'
    })

if __name__ == '__main__':
  lock = RateLimiter(max_messages=10, every_seconds=60)
  fb = FreebaseAPI(rate_limit_lock=lock)
  actor = fb.all_actors()[0]
  print actor['name']
  for movie in fb.movies(actor['name']):
    print movie['name']

