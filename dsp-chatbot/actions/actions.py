# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from tkinter import EventType
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction
from rasa_sdk.executor import CollectingDispatcher

import requests

def getUserName(userId):
    response = requests.get('http://internal-cnn-lb-rg-awsk8s-dsp-1848782492.cn-north-1.elb.amazonaws.com.cn/api/master-data/users/query-username?userIds='+userId)
    if response.status_code == 200:
        data = response.json()
        return data.get('body', {}).get(userId, userId)
    else:
        print(f"Request failed with status code {response.status_code}")
    return ""

def getCustomerPhone(customerId):
    response = requests.get('http://internal-cnn-lb-rg-awsk8s-dsp-1848782492.cn-north-1.elb.amazonaws.com.cn/api/master-data/customers/'+customerId)
    if response.status_code == 200:
        data = response.json()
        print(data.get('body'))
        return data.get('body').get('dspManagerMobile')
    else:
        print(f"Request failed with status code {response.status_code}")
    return ""
def getUserPhone(userId):
    response = requests.get('http://internal-cnn-lb-rg-awsk8s-dsp-1848782492.cn-north-1.elb.amazonaws.com.cn/api/master-data/users/'+userId+'/customer')
    if response.status_code == 200:
        data = response.json()
        print(data)
        mobile = data.get('body').get('mobile')
        print(mobile)
        return mobile
    else:
        print(f"Request failed with status code {response.status_code}")
    return ""  

def isAdmin(userId,customerId):
    customer_phone = getCustomerPhone(customerId)
    mobile = getUserPhone(userId)
    if customer_phone == mobile:
        return "当前登陆账号已是贵司管理员，无需申请。如需将管理员权限转移至其他用户，请先联系销售或订单员确认，由渠道共享中心完成管理员变更"
    else:
        return "贵司已有管理员，如需变更，请先联系销售或订单员确认，由渠道共享中心完成管理员变更"
class HelpOptionsAction(Action):

    def name(self) -> Text:
        return "action_help_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:

        buttons = [
            {"title": "如何申请角色", "payload": "如何申请角色"},
            {"title": "如何登录MyCP微信小程序", "payload": "如何登录MyCP微信小程序"},
            {"title": "订单及支付", "payload": "订单及支付"},
            {"title": "业绩及激励", "payload": "业绩及激励"},
            {"title": "市场及活动", "payload": "市场及活动"},
        ]

        userId = tracker.latest_message['metadata'].get('userId')

        # 使用buttons参数构造包含按钮的消息
        dispatcher.utter_message(text=f"欢迎使用施耐德经销商管理平台MyCP，请问您需要使用系统的哪个功能，当前登录用户：{getUserName(userId)}", buttons=buttons)


class HelpReturnAction(Action):

    def name(self) -> Text:
        return "action_return_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:

        buttons = [
            {"title": "退换货管理", "payload": "退换货管理"},
            {"title": "物流退返", "payload": "物流退返"},
            {"title": "商务退返", "payload": "商务退返"},
        ]

        userId = tracker.latest_message['metadata'].get('userId')
        # 使用buttons参数构造包含按钮的消息
        dispatcher.utter_message(text=f"售后及支持目前包含以下三个功能，您想使用的是？，当前登录用户：{getUserName(userId)}", buttons=buttons)


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):

        # 触发另一个动作，这个动作可以是故事的起点
        return [FollowupAction("action_first_step_in_story")]
        #dispatcher.utter_message(text=f"抱歉，我们暂时无法支持此类问题的答疑，如有需要可联系人工获取支持。")

class HiApplyRole(Action):

    def name(self) -> Text:
        return "action_hi_apply_role"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:

        buttons = [
            {"title": "如何申请角色", "payload": "如何申请角色"},
            {"title": "如何登录MyCP微信小程序", "payload": "如何登录MyCP微信小程序"}
        ]
        dispatcher.utter_message(text=f"欢迎使用施耐德电气客户服务平台引导工具，您是否需要咨询：", buttons=buttons)


class ApplyRole(Action):

    def name(self) -> Text:
        return "action_apply_role"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:

        buttons = [
            {"title": "管理员角色", "payload": "管理员角色"},
            {"title": "其他业务角色", "payload": "其他业务角色"}
        ]
        dispatcher.utter_message(text=f"请问您需要申请：", buttons=buttons)


class WhatIsAdmin(Action):

    def name(self) -> Text:
        return "action_admin_is"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:
        dispatcher.utter_message(text=f"每家公司在平台指定唯一管理员用户，该用户具有本平台最大的功能和数据权限，同时需负责贵司业务员在本平台的准入准出、角色审批等")


class ApplyAdmin(Action):

    def name(self) -> Text:
        return "action_apply_admin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:
        userId = tracker.latest_message['metadata'].get('userId')
        customerId = tracker.latest_message['metadata'].get('customerId')
        dispatcher.utter_message(text=f"{isAdmin(userId,customerId)}")
# class ActionStartSpecificStory(Action):
#     def name(self) -> Text:
#         return "action_start_specific_story"
#
#     def run(self, dispatcher, tracker, domain):
#         # 在这里你可以执行特定故事的逻辑，或者直接触发故事中的第一个动作
#         return [FollowupAction("action_first_step_in_story")]

#
# class ActionDefaultFallback(Action):
#     """Executes the fallback action and goes back to the previous state
#     of the dialogue"""
#
#     def name(self):
#         return 'action_default_fallback'
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[EventType]:
#
#         buttons = [
#             {"title": "签约及授权", "payload": "签约及授权"},
#             {"title": "售后及支持", "payload": "售后及支持"},
#             {"title": "订单及支付", "payload": "订单及支付"},
#             {"title": "业绩及激励", "payload": "业绩及激励"},
#             {"title": "市场及活动", "payload": "市场及活动"},
#         ]
#
#         # 使用buttons参数构造包含按钮的消息
#         dispatcher.utter_message(text="欢迎使用施耐德经销商管理平台MyCP，请问您需要使用系统的哪个功能", buttons=buttons)

if __name__ == '__main__':
    customer_phone = getCustomerPhone('631416479402059776')
    print('customer_phone:',customer_phone)
    mobile = getUserPhone('3039113916488876032')