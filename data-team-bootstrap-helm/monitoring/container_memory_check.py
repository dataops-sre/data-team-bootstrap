#!/usr/bin/env python
import psutil
import sys

CGROUP_MEM_LIMIT_FILE = '/sys/fs/cgroup/memory/memory.limit_in_bytes'

def main():
  mem_total = 0
  f = open(CGROUP_MEM_LIMIT_FILE, "r")
  container_cgroup_limit = float(f.read())
  f.close()

  for p in psutil.process_iter(): 
    p_mem = p.memory_full_info()
    mem_total = mem_total + (p_mem.rss - p_mem.shared)

  mem_used_percent = (mem_total/container_cgroup_limit) * 100
  print("container cgroup limit : {0}, total container process memory : {1}".format(container_cgroup_limit, mem_total))
  print("total memory use percentage {0}".format(mem_used_percent))
  if mem_used_percent > 90:
    sys.exit(1)
  else:
    sys.exit(0)

if __name__== "__main__":
  main()