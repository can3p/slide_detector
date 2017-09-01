import os
import sys
import datetime
import re
import string

def str_to_d(str):
    return datetime.datetime.strptime(str, "%H:%M:%S.%f")

def str_to_fname(str):
    return string.replace(str, '.pickle', '')

def parse_generated_timings(filename):
    timings = []
    with open(filename, 'r') as f:
        for line in f:
            parts = re.split('\s+', line)
            timings.append([str_to_fname(parts[1]), str_to_d(parts[2])])

    return timings

def generate_durations_list(in_timings, total_duration):
    current_filename = in_timings[0][0]
    current_ts = str_to_d('00:00:00.000')
    out_timings = []

    for timing in in_timings:
        filename = timing[0]
        if filename != current_filename:
            out_timings.append([current_filename, timing[1] - current_ts])
            current_ts = timing[1]
            current_filename = timing[0]

    out_timings.append([current_filename, total_duration - current_ts])

    return out_timings

def write_ffmpeg_file(timings, out_file):
    with open(out_file, 'w') as f:
        for timing in timings:
            f.write('file \'{}\'\n'.format(timing[0]))
            f.write('duration {}\n'.format(str(timing[1])))
    


in_file = sys.argv[1]
out_file = sys.argv[2]
total_duration = str_to_d(sys.argv[3])

in_timings = parse_generated_timings(in_file)
out_timings = generate_durations_list(in_timings, total_duration)

write_ffmpeg_file(out_timings, out_file)
