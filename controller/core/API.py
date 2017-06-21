# -*- coding:utf-8 -*-
# !/usr/bin/env python
#
# Author: Shawn.T
# Email: shawntai.ds@gmail.com
#
# this is the Interface package of Ansible2 API
#

import json
from ansible.plugins.callback import CallbackBase
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor

loader = DataLoader()  # 用来加载解析yaml文件或JSON内容,并且支持vault的解密
variable_manager = VariableManager()  # 管理变量的类,包括主机,组,扩展等变量,之前版本是在 inventory 中的
inventory = Inventory(loader=loader, variable_manager=variable_manager)
variable_manager.set_inventory(inventory)  # 根据 inventory 加载对应变量


class Options(object):
    '''
     这是一个公共的类,因为ad-hoc和playbook都需要一个options参数
     并且所需要拥有不同的属性,但是大部分属性都可以返回None或False
     因此用这样的一个类来省去初始化大一堆的空值的属性
     '''

    def __init__(self):
        self.connection = "local"
        self.forks = 1
        self.check = False

    def __getattr__(self, name):
        return None


options = Options()


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def __init__(self):
        self.res = None

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        res = json.dumps({host.name: result._result}, indent=4)
        self.res = result._result
        # return result._result



def run_adhoc():
    variable_manager.extra_vars = {"ansible_ssh_user": "root", "ansible_ssh_pass": "xxx"}  # 增加外部变量
    # 构建pb, 这里很有意思, 新版本运行ad-hoc或playbook都需要构建这样的pb, 只是最后调用play的类不一样
    # :param name: 任务名,类似playbook中tasks中的name
    # :param hosts: playbook中的hosts
    # :param tasks: playbook中的tasks, 其实这就是playbook的语法, 因为tasks的值是个列表,因此可以写入多个task
    play_source = {"name": "Ansible Ad-Hoc", "hosts": "192.168.93.128", "gather_facts": "no",
                   "tasks": [{"action": {"module": "shell", "args": "ifconfig"}}]}
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    tqm = None
    callback = ResultCallback()
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=None,
            stdout_callback=callback,
            run_tree=False,
        )
        result = tqm.run(play)
        # print result
        res = callback.res
        # print res,type(res)
        for k,v in res.items():
            print k,v

    finally:
        if tqm is not None:
            tqm.cleanup()


if __name__ == '__main__':
    run_adhoc()
