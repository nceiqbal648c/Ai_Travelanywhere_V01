[app]
title = AI Travel Anywhere
package.name = aitravelanywhere
package.domain = org.ia
source.dir = .
source.include_exts = py,png,jpg,jpeg,html,css,js,txt,sh
source.include_patterns = templates/*, static/*
version = 0.0.7

requirements = python3,flask,yt-dlp,requests,jinja2,werkzeug,itsdangerous,click,hostpython3

orientation = portrait
fullscreen = 1

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.archs = arm64-v8a
android.entrypoint = app.py
