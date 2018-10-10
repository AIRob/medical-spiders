#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'AIRob'


from toutiaopjt.middlewares.resource import PROXIES
import random

class RandomProxy(object):
    def process_request(self,request,spider):
        proxy = random.choice(PROXIES) 
        request.meta['proxy'] = 'http://%s' %proxy
