# SimpleDownloader

A simple app to speed up installation of softwre of a fresh Windows 10/11 install.
This software provides a simple GUI to select some commonly used programs for dowload.

Internally, `winget` is used to download and install specified programs.
If a selected program already exists on the system, winget will attempt to upgrade it
