#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'AIRob'

from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from jbkpjt.middlewares.resource import UserAgents
import random

class RandomUserAgent(UserAgentMiddleware):
    def process_request(self,request,spider):
        ua = random.choice(UserAgents)
        request.headers.setdefault('User-Agent', ua)

