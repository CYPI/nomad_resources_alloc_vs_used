#!/usr/bin/env python

import requests
import sys
import json

nomad_api = 'https://localhost:4646'

def api_call(endpoint):
        try:
            response = requests.request("GET", nomad_api + endpoint)
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            return '{}'

if __name__ == '__main__':

    jobs = api_call('/v1/allocations')
    print "{0:37s} {1:10s} {2:15s} {3:10s} {4:10s}".format("job", "CPU stat",
    "alloc CPU", "Mem stat", "alloc Mem")
    for job in jobs:
        job_name = job['JobID']
        job_allocation_id = job['ID']
        try:
            job_stats = api_call('/v1/client/allocation/' + job_allocation_id + '/stats')
            job_cpustats = job_stats['ResourceUsage']['CpuStats']['Percent']
            job_memstats = job_stats['ResourceUsage']['MemoryStats']['Cache']
            job_resources = api_call('/v1/job/' + job_name)
            resources = job_resources['TaskGroups'][0]['Tasks'][0]['Resources']
            print "{0:30s} {1:10d} {2} {3:10d} {4} {5:10d} {6} {7:10d} {8}".format(job_name,
            int(job_cpustats * 100), "%", resources['CPU'], "CPU unit", job_memstats / 1024, "MB",
            resources['MemoryMB'], "MB")
        except:
            pass
