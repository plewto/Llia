# proxy_test
# 2016.04.22

from __future__ import print_function
from llia.proxy import LliaProxy


def test1(config):
    proxy = LliaProxy(config)
    # print(proxy.x_boot_server("local"))
    # print(proxy.x_boot_server("internal"))
    # print(proxy.x_kill_all_servers())
    # print(proxy.x_boot_server())
    # print(proxy.q_running_servers())
    # proxy.x_ping()
    trans = proxy.osc_transmitter
    # proxy.add_synth("ORGN", 1)
    trans.send_raw("/llia/ORGN/1/ping")
    

    

