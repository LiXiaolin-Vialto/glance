# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render
from . import (VERSION, RELEASE_DATE)

logger = logging.getLogger(__name__)


def home(request):
    """
    renders home page and set resp heades for deployment check
    """
    if request.method == 'GET':
        logger.info('[home] index is visted.')
        if request.user.is_authenticated():
            resp = render(request, 'index.html', {})
        else:
            resp = render(request, 'login.html', {})
        resp.setdefault('Version', VERSION)
        resp.setdefault('Release-Date', RELEASE_DATE)
        return resp
