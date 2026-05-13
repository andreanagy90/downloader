python3 -m pip show yt-dlp | grep Location
python3 -c "import pkgutil; print([m.module_finder.path for m in pkgutil.iter_modules() if m.name=='yt_dlp'])"
which -a yt-dlp
