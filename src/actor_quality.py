#!/usr/bin/env python
import sys
import csv
from sets import Set
from apiclient import RateLimiter
from rotten_tomatoes import RTApi
from freebase import FreebaseAPI

rt_lock = RateLimiter(max_messages=5, every_seconds=3)
rt = RTApi(rate_limit_lock=rt_lock)

fb_lock = RateLimiter(max_messages=10, every_seconds=3)
fb = FreebaseAPI(rate_limit_lock=fb_lock)

movies_file = 'movies_v2.csv'

def existing_actors():
  actors = Set()
  with open(movies_file, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      actors.add(row[1])
  return actors


def export_all_movies_csv():
  with open(movies_file, "ab") as csvfile:
    moviewriter = csv.writer(csvfile)

    moviewriter.writerow([
      '#actor_mid','name','actor_notable',
      'movie_mid','movie_id','movie_name',
      'movie_notable','rating','runtime',
      'year','imdb',
      'audience_score', 'audience_rating', 
      'critics_score', 'critics_rating'
      ])

    processed_actors = existing_actors()

    for actor in fb.all_actors():
    #for actor in [{'name':'Steve Martin'}]:

      if actor['name'] in processed_actors:
        print "skip %(name)s" % actor
        continue
      else:
        print "process %(name)s" % actor
      #sys.exit()

      try:
        movies = fb.movies(actor['name'])
        for movie in movies:
          try:
            rt_result = rt.movie(movie['name'])
            if len(rt_result['movies']) > 0:
              _rt_movie = rt_result.get('movies')
              rt_movie = _rt_movie[0] if len(_rt_movie)>0 else {}
              
              _imdb = rt_movie.get('alternate_ids')
              imdb = None if _imdb==None else _imdb.get('imdb')

              _notable = actor.get('notable')
              actor_notable = None if _notable==None else _notable.get('name')

              _notable = movie.get('notable')
              movie_notable = None if _notable==None else _notable.get('name')

              if rt_movie != None:
                rt_rating = rt_movie['ratings']
                moviewriter.writerow([
                  actor.get('mid'),
                  actor.get('name'),
                  actor_notable,
                  movie.get('mid'),
                  movie.get('id'),
                  movie.get('name'),
                  movie_notable,
                  rt_movie.get('mpaa_rating'),
                  rt_movie.get('runtime'),
                  rt_movie.get('year'),
                  imdb,
                  rt_rating.get('audience_rating'),
                  rt_rating.get('critics_score'),
                  rt_rating.get('critics_rating'),
                  rt_rating.get('audience_score'),
                  rt_rating.get('audience_rating')
                  ])
            print '.',
            sys.stdout.flush()
          except UnicodeEncodeError, e:
            print
        print
        sys.stdout.flush()
      except UnicodeEncodeError, e:
        print


if __name__ == '__main__':

  #print rt.search('lists/movies.json', {})
  export_all_movies_csv()

