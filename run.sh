#!/bin/bash
django-admin makemessages -a && django-admin compilemessages \
  && docker-compose -f docker-compose.dev.yml up -d --build