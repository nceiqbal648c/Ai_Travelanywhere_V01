[Name: Build APK

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Java and System Dependencies
        run: |
          sudo apt update
          sudo apt install -y openjdk-17-jdk zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libssl-dev libffi-dev libgdbm-dev libsqlite3-dev uuid-dev togl tk-dev library-utils libgstreamer1.0-dev glib-2.0-dev libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libgl1-mesa-dev libgles2-mesa-dev libgstreamer-plugins-base1.0-dev lld

      - name: Install Buildozer and Cython
        run: |
          pip install --upgrade pip
          pip install buildozer cython setuptools

      - name: Build APK with Buildozer
        run: |
          # The yes command automatically accepts the Android SDK/NDK licenses
          yes | buildozer android debug

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: AI_Travel_Anywhere_APK
          path: .buildozer/android/platform/build-armeabi-v7a_arm64-v8a/dists/*/build/outputs/apk/debug/*.apk
