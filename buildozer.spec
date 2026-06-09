[app]

# অ্যাপের নাম এবং প্যাকেজ ডিটেইলস
title = AI Travel Anywhere
package.name = aitravelanywhere
package.domain = org.ia
source.dir = .
source.include_exts = py,png,jpg,jpeg,html,css,js,json
version = 0.0.7

# 🌟 আইকন সেটআপ (আপনার প্রজেক্ট ফোল্ডারে icon.png নামের একটি ছবি থাকতে হবে)
icon.filename = %(source.dir)s/icon.png

# 🌟 প্রয়োজনীয় রিকোয়ারমেন্টস (এখানে kivy এবং android যুক্ত করা হয়েছে)
requirements = python3,kivy,flask,yt-dlp,requests,jinja2,werkzeug,itsdangerous,click,android

orientation = portrait
fullscreen = 1

# অ্যান্ড্রয়েড পারমিশনস
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# 🌟 অ্যান্ড্রয়েড এপিআই লেভেল (গিটহাব বিল্ডের জন্য এটি ফিক্সড করা জরুরি)
android.api = 33
android.minapi = 21
android.ndk = 25b

# অ্যান্ড্রয়েড আর্কিটেকচার সেটআপ (arm64 এর পাশাপাশি armeabi ও দেওয়া ভালো সব ফোনের জন্য)
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
