#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

import os
import re

from datetime import datetime

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}

# def get_last_logfile(log_dir):
#     return "%s/nginx-access-ui.log-%s" % (log_dir, get_max_date(log_dir))


def get_log_file(log_dir):
    return "%s/nginx-access-ui.log-%s" % (log_dir, get_max_date(log_dir))


def get_max_date(log_dir):
    max_date = 00000000
    for file in get_all_log_files(log_dir):
        result = re.search("\d{8}$", file)
        if result:
            if int(result.group(0)) > max_date:
                max_date = int(result.group(0))
    return max_date


def get_all_log_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def main():
    # current_date = datetime.today().strftime('%Y.%m.%d')
    # print(current_date)
    with open(get_log_file(config["LOG_DIR"])) as f:
        first_line = f.readline()

    print(first_line)


if __name__ == "__main__":
    main()
