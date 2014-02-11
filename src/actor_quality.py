#!/usr/bin/env python
import sys
import csv
from apiclient import RateLimiter
from rotten_tomatoes import RTApi
from freebase import FreebaseAPI

rt_lock = RateLimiter(max_messages=5, every_seconds=3)
rt = RTApi(rate_limit_lock=rt_lock)

fb_lock = RateLimiter(max_messages=10, every_seconds=3)
fb = FreebaseAPI(rate_limit_lock=fb_lock)

actors = fb.all_actors()
#actors = actors[63:]
with open("movies.csv", "wb") as csvfile:
  moviewriter = csv.writer(csvfile)
  for actor in actors:
    print actor['name'],
    try:
      movies = fb.movies(actor['name'])
      for movie in movies:
        try:
          rt_result = rt.movie(movie['name'])
          if len(rt_result['movies']) > 0:
            rt_movie = rt_result['movies'][0]
            rt_rating = rt_movie['ratings']
            moviewriter.writerow([
              "%(name)s" % actor,
              "%(name)s" % movie,
              "%(year)s" % rt_movie,
              "%(audience_score)s" % rt_rating])
          print '.',
          sys.stdout.flush()
        except UnicodeEncodeError, e:
          print
      print
      sys.stdout.flush()
    except UnicodeEncodeError, e:
      print
