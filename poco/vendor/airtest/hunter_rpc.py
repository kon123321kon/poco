# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-11 14:34:46

from poco.utils.exception_transform import member_func_exception_transform, transform_node_has_been_removed_exception
from poco.interfaces.rpc import RpcInterface, RpcRemoteException, RpcTimeoutException
from poco.shortcut.airtester import AirtestInputer, AirtestScreen
from poco.interfaces.ui import UIHierarchyInterface
from hrpc.exceptions import \
    RpcRemoteException as HRpcRemoteException, \
    RpcTimeoutException as HRpcTimeoutException
from hunter_cli.rpc.client import HunterRpcClient


@member_func_exception_transform(HRpcRemoteException, RpcRemoteException)
@member_func_exception_transform(HRpcTimeoutException, RpcTimeoutException)
class HunterRpc(RpcInterface):
    def __init__(self, hunter, poco):
        self.rpc_client = HunterRpcClient(hunter)
        self.rpc_client.set_timeout(25)  # 把timeout设置长一点，避免有些游戏切场景时耗时太久，来不及响应rpc请求
        self.remote_poco = self.rpc_client.remote('poco-uiautomation-framework-2')
        # dumper = self.remote_poco.dumper
        selector = self.remote_poco.selector
        attributor = self.remote_poco.attributor
        # screen = self.remote_poco.screen
        RpcInterface.__init__(
            self,
            uihierarchy=RemotePocoUI(selector, attributor),
            inputer=AirtestInputer(poco),
            screen=AirtestScreen(),
        )

    def evaluate(self, obj_proxy):
        return self.rpc_client.evaluate(obj_proxy)


class RemotePocoUI(UIHierarchyInterface):

    def __init__(self, selector, attributor):
        self.selector = selector
        self.attributor = attributor

    # node/hierarchy interface
    @transform_node_has_been_removed_exception
    def getattr(self, nodes, name):
        return self.attributor.getAttr(nodes, name)

    @transform_node_has_been_removed_exception
    def setattr(self, nodes, name, value):
        return self.attributor.setAttr(nodes, name, value)

    def select(self, query, multiple):
        return self.selector.select(query, multiple)
