#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

import os
import re

from collections import namedtuple

config = {"REPORT_SIZE": 1000, "REPORT_DIR": "./reports", "LOG_DIR": "./log"}

table = []


def get_last_log(log_dir):
    filename_options = namedtuple("filename_options", ["path", "last_date"])
    last_log_file = filename_options(
        "%s/nginx-access-ui.log-" % log_dir, str(get_max_date(log_dir))
    )
    return last_log_file


def get_max_date(log_dir):
    max_date = int()
    for file in get_log_files_list(log_dir):
        result = re.search("\d{8}$", file)
        if result:
            if int(result.group(0)) > max_date:
                max_date = int(result.group(0))
    return max_date


def get_log_files_list(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def main():
    last_log_file = get_last_log(config["LOG_DIR"])
    with open(last_log_file.path + last_log_file.last_date) as f:
        for line in f:
            time = re.search("\d+\.\d+$", line).group(0)
            try:
                url = re.search('"\w+\s(.*)\sHTTP', line).group(1)
            except:
                continue
            if len(table) == 0:
                table.append({"url": url, "time": time, "count": 1})


if __name__ == "__main__":
    main()
