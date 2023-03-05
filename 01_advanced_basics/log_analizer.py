#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

import os
import re

from collections import namedtuple
from decimal import Decimal
from statistics import median

config = {"REPORT_SIZE": 1000, "REPORT_DIR": "./reports", "LOG_DIR": "./log"}

pre_table = {}
result_table = []
full_count = 0
full_time = 0


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
            time = Decimal(re.search("\d+\.\d+$", line).group(0))
            try:
                url = re.search('"\w+\s(.*)\sHTTP', line).group(1)
            except:
                continue
            if len(pre_table) == 0:
                pre_table[url] = [time]
            else:
                if url not in pre_table:
                    pre_table[url] = [time]
                else:
                    pre_table[url].append(time)

    for row in pre_table:
        full_count =+ len(pre_table[row])
        full_time =+ sum(pre_table[row])

        print(full_count)
        print(full_time)

    for row in pre_table:
        result_table.append(
            {
                "url": row,
                "count": len(pre_table[row]),
                "time_max": max(pre_table[row]),
                "time_sum": sum(pre_table[row]),
                "time_avg": sum(pre_table[row]) / len(pre_table[row]),
                "count_perc": len(pre_table[row]) / (full_count / 100),
                "time_perc": sum(pre_table[row]) / (full_time / 100),
                "time_med": median(pre_table[row])
            })

    very_result_table = sorted(result_table, key=lambda d: d['count'], reverse=True)

    print(very_result_table[:5])
    # import pdb; pdb.set_trace()


if __name__ == "__main__":
    main()
