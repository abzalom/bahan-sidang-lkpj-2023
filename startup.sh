#!/bin/bash
sudo sysctl fs.inotify.max_user_watches=524288
streamlit run main.py