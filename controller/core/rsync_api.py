# -*- coding: UTF-8 -*-

import ansible.runner


def get_info(ip):
    data = {}
    runner = ansible.runner.Runner(module_name='setup', module_args='', pattern='%s' % ip, forks=2)
    datastructure = runner.run()
    sn = datastructure['contacted'][ip]['ansible_facts']['ansible_product_serial']
    host_name = datastructure['contacted'][ip]['ansible_facts']['ansible_hostname']

    description = datastructure['contacted'][ip]['ansible_facts']['ansible_lsb']['description']
    ansible_machine = datastructure['contacted'][ip]['ansible_facts']['ansible_machine']
    sysinfo = '%s %s' % (description, ansible_machine)

    os_kernel = datastructure['contacted'][ip]['ansible_facts']['ansible_kernel']

    cpu = datastructure['contacted'][ip]['ansible_facts']['ansible_processor'][1]
    cpu_count = datastructure['contacted'][ip]['ansible_facts']['ansible_processor_count']
    cpu_cores = datastructure['contacted'][ip]['ansible_facts']['ansible_processor_cores']
    mem = datastructure['contacted'][ip]['ansible_facts']['ansible_memtotal_mb']

    ipadd_in = datastructure['contacted'][ip]['ansible_facts']['ansible_all_ipv4_addresses'][0]
    disk = datastructure['contacted'][ip]['ansible_facts']['ansible_devices']['sda']['size']
    # print sysinfo
    data['sn'] = sn
    data['sysinfo'] = sysinfo
    data['cpu'] = cpu
    data['cpu_count'] = cpu_count
    data['cpu_cores'] = cpu_cores
    data['mem'] = mem
    data['disk'] = disk
    data['ipadd_in'] = ipadd_in
    data['os_kernel'] = os_kernel
    data['host_name'] = host_name

    return data


def get_ulimit(ip):
    # 最大文件打开数
    runner = ansible.runner.Runner(module_name='shell', module_args='ulimit -n', pattern='%s' % ip, forks=2)
    datastructure = runner.run()
    result = datastructure['contacted'][ip]['stdout']

    return result


def get_uptime(ip):
    # 运行时间
    runner = ansible.runner.Runner(module_name='shell', module_args='uptime', pattern='%s' % ip, forks=2)
    datastructure = runner.run()
    result = datastructure['contacted'][ip]['stdout']
    try:
        result = result.split('up')[1].split('days')[0]
        result = int(result)
    except:
        result = 0
    return result


def get_service_port(ip):
    # 获取服务端口信息
    # 数据结构 {服务名:[端口], ...}
    runner = ansible.runner.Runner(module_name='shell', module_args='netstat -nptl', pattern='%s' % ip, forks=2)
    datastructure = runner.run()
    data = datastructure['contacted'][ip]['stdout']
    data = data.split('\n')

    result = {}
    for dt in data[2:]:
        dt = dt.split()
        if dt[3].count(':') == 1:
            port = dt[3].split(':')[1]
            service = dt[6].split('/')[1]
            if service not in result:
                result[service] = [port]
            else:
                result[service].append(port)
    return result


def rsync_file(ip):
    # 最大文件打开数
    args = "src=/opt/django/skyoms/ dest=/opt/django/skyoms/ delete=yes"
    runner = ansible.runner.Runner(module_name='synchronize', module_args="%s" % args, pattern='%s' % ip, forks=2)
    datastructure = runner.run()
    # print datastructure
    result = datastructure['contacted'][ip]

    return result

if __name__ == '__main__':
    data = rsync_file('192.168.93.128')
    print data
