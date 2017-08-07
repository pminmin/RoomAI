#!/bin/python

from setuptools import setup

setup(  name        = "roomai",
        version     = "snapshot",
        description = "A toolkit for developing and comparing imperfect information game bots",
        url         = "https://github.com/roomai/RoomAI",
        author      = "algorithmdog",
        author_email= "lili1987mail@gmail.com",
        license     = "MIT",
        packages    = ["roomai","roomai.kuhn","roomai.common","roomai.texas","roomai.fivecardstud","roomai.sevenking","roomai.doudizhu"],
        zip_safe    = False)
