# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, requests, random, re
from pprint import pprint
import calendar
from datetime import date

from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.conf import settings


message_max_length = 640

curriculum = {
    "2017-09-09": [
        "13:50 Математичні та імітаційні моделі складних систем\nЛекція\t\tа.345\t\tКотетунов В.Ю",
        "15:20 Мережні технології\nЛаба\t\tа.345\t\tЦюцюра С.В."
    ],
    "2017-09-10": [
        "09:00 1Математичні та імітаційні моделі складних систем\nЛекція\t\tа.345\t\tКотетунов В.Ю",
        "10:30 Мережні технології\nЛаба\t\tа.345\t\tЦюцюра С.В.\n"
    ],
    "2017-09-11": [
        "09:00 2Математичні та імітаційні моделі складних систем\nЛекція\t\tа.345\t\tКотетунов В.Ю",
        "10:30 Мережні технології\nЛаба\t\tа.345\t\tЦюцюра С.В.\n"
    ],
    "2017-09-12": [
        "09:00 3Математичні та імітаційні моделі складних систем\nЛекція\t\tа.345\t\tКотетунов В.Ю",
        "10:30 Мережні технології\nЛаба\t\tа.345\t\tЦюцюра С.В.\n"
    ],
    "2017-09-13": [
        "09:00 Математичні та імітаційні моделі складних систем\nЛекція\t\tа.345\t\tКотетунов В.Ю",
        "10:30 Мережні технології\nЛаба\t\tа.345\t\tЦюцюра С.В.\n"
    ],
    "2017-09-14": [
        "09:00 Математичні та імітаційні моделі складних систем\nЛекція\t\tа.345\t\tКотетунов В.Ю",
        "10:30 Мережні технології\nЛаба\t\tа.345\t\tЦюцюра С.В.\n"
    ],
    "2017-09-18": [
        "09:00 3434Математичні та імітаційні моделі складних систем\nЛекція\t\tа.345\t\tКотетунов В.Ю",
        "10:30 Мережні технології\nЛаба\t\tа.345\t\tЦюцюра С.В.\n"
    ],
    "2017-09-19": [
        "09:00 2342Математичні та імітаційні моделі складних систем\nЛекція\t\tа.345\t\tКотетунов В.Ю",
        "10:30 Мережні технології\nЛаба\t\tа.345\t\tЦюцюра С.В.\n"
    ],
    "2017-09-20": [
        "09:00 54Математичні та імітаційні моделі складних систем\nЛекція\t\tа.345\t\tКотетунов В.Ю",
        "10:30 Мережні технології\nЛаба\t\tа.345\t\tЦюцюра С.В.\n"
    ],
    "2017-09-21": [
        "09:00 453Математичні та імітаційні моделі складних систем\nЛекція\t\tа.345\t\tКотетунов В.Ю",
        "10:30 Мережні технології\nЛаба\t\tа.345\t\tЦюцюра С.В.\n"
    ],
    "2017-09-22": [
        "09:00 34Математичні та імітаційні моделі складних систем\nЛекція\t\tа.345\t\tКотетунов В.Ю",
        "10:30 Мережні технології\nЛаба\t\tа.345\t\tЦюцюра С.В.\n"
    ]
}
weekdays = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "НД"]

def post_request(fbid):
    params = {
        "access_token": settings.PAGE_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages'
    response_msg = json.dumps(
        {
            "recipient": {"id": fbid},
            "message": {
                "text": "Дізнатися розклад:",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "На сьогодні",
                        "payload": "PAYLOAD_TODAY"
                    },
                    {
                        "content_type": "text",
                        "title": "На завтра",
                        "payload": "PAYLOAD_NEXTDAY"
                    },
                    {
                        "content_type": "text",
                        "title": "На цей тиждень",
                        "payload": "PAYLOAD_WEEK"
                    },
                    {
                        "content_type": "text",
                        "title": "На наступний тиждень",
                        "payload": "PAYLOAD_NEXTWEEK"
                    }
                ]
            }
        }
    )
    status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
    pprint(status.json())


def post_today(fbid):
    params = {
        "access_token": settings.PAGE_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    response_text = ""
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages'
    today = date.today()
    #today = today.replace(day=today.day+2)
    #cal = calendar.Calendar()
    # for day in cal.itermonthdates(2017, 9):
    #     if today == day:
    #         print day
    # print "END FIRST"
    #print calendar.weekheader(3)
    #print today.timetuple().tm_wday
    # for day in cal.itermonthdays2(2017, 9):
    #     print day
    # print "END SEC"
    # for day in cal.itermonthdays(2017, 9):
    #     print day
    if today.isoformat() in curriculum and today.timetuple().tm_wday < 5:
        response_text = "\n\n".join(curriculum[today.isoformat()])
    else:
        response_text = "Сьогодні пар немає"
    response_msg = json.dumps(
        {
            "recipient": {"id": fbid},
            "message": {
                "text": "Пари на {0} {1}\n\n{2}".format(
                    weekdays[today.timetuple().tm_wday],
                    today.strftime("%d.%m.%y"),
                    response_text),
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "На сьогодні",
                        "payload": "PAYLOAD_TODAY"
                    },
                    {
                        "content_type": "text",
                        "title": "На завтра",
                        "payload": "PAYLOAD_NEXTDAY"
                    },
                    {
                        "content_type": "text",
                        "title": "На цей тиждень",
                        "payload": "PAYLOAD_WEEK"
                    },
                    {
                        "content_type": "text",
                        "title": "На наступний тиждень",
                        "payload": "PAYLOAD_NEXTWEEK"
                    }
                ]
            }
        }
    )
    status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
    pprint(status.json())


def post_nextday(fbid):
    params = {
        "access_token": settings.PAGE_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    response_text = ""
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages'
    today = date.today().replace(day=date.today().day+1)
    if today.isoformat() in curriculum and today.timetuple().tm_wday < 5:
        response_text = "\n\n".join(curriculum[today.isoformat()])
    else:
        response_text = "В цей день пар немає"
    response_msg = json.dumps(
        {
            "recipient": {"id": fbid},
            "message": {
                "text": "Пари на {0} {1}\n\n{2}".format(
                    weekdays[today.timetuple().tm_wday],
                    today.strftime("%d.%m.%y"),
                    response_text),
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "На сьогодні",
                        "payload": "PAYLOAD_TODAY"
                    },
                    {
                        "content_type": "text",
                        "title": "На завтра",
                        "payload": "PAYLOAD_NEXTDAY"
                    },
                    {
                        "content_type": "text",
                        "title": "На цей тиждень",
                        "payload": "PAYLOAD_WEEK"
                    },
                    {
                        "content_type": "text",
                        "title": "На наступний тиждень",
                        "payload": "PAYLOAD_NEXTWEEK"
                    }
                ]
            }
        }
    )
    status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
    pprint(status.json())


def post_week(fbid):
    params = {
        "access_token": settings.PAGE_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    response_text = ""
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages'
    today = date.today()
    if today.timetuple().tm_wday > 4:
        response_text = "На цьому тижні більше немає пар"
    else:
        if today.isoformat() in curriculum and today.timetuple().tm_wday < 5:
            response_text = "\n\n".join(curriculum[today.isoformat()])
            response_text = "Пари на {0} {1}\n\n{2}".format(
                weekdays[today.timetuple().tm_wday],
                today.strftime("%d.%m.%y"),
                response_text)
        while today.timetuple().tm_wday < 4:
            today = today.replace(day=today.day+1)
            if today.isoformat() in curriculum and today.timetuple().tm_wday < 5:
                curri = "\n\n".join(curriculum[today.isoformat()])
                response_text = "{0}\n\n\nПари на {1} {2}\n\n{3}".format(
                    response_text,
                    weekdays[today.timetuple().tm_wday],
                    today.strftime("%d.%m.%y"),
                    curri)
            else:
                response_text = "{0}\n\n\nПари на {1} {2}\n\n{3}".format(
                    response_text,
                    weekdays[today.timetuple().tm_wday],
                    today.strftime("%d.%m.%y"),
                    "В цей день пар немає")
    messages = response_text.split('\n\n\n')
    for message in messages:
        response_msg = json.dumps(
            {
                "recipient": {"id": fbid},
                "message": {
                    "text": message,
                    "quick_replies": [
                        {
                            "content_type": "text",
                            "title": "На сьогодні",
                            "payload": "PAYLOAD_TODAY"
                        },
                        {
                            "content_type": "text",
                            "title": "На завтра",
                            "payload": "PAYLOAD_NEXTDAY"
                        },
                        {
                            "content_type": "text",
                            "title": "На цей тиждень",
                            "payload": "PAYLOAD_WEEK"
                        },
                        {
                            "content_type": "text",
                            "title": "На наступний тиждень",
                            "payload": "PAYLOAD_NEXTWEEK"
                        }
                    ]
                }
            }
        )
        status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
        pprint(status.json())


def post_nextweek(fbid):
    params = {
        "access_token": settings.PAGE_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    response_text = ""
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages'
    today = date.today()
    if today.timetuple().tm_wday == 0:
        today = today.replace(day=today.day+1)
    while today.timetuple().tm_wday != 0:
        today = today.replace(day=today.day+1)
        print today

    if today.isoformat() in curriculum and today.timetuple().tm_wday < 5:
        response_text = "\n\n".join(curriculum[today.isoformat()])
        response_text = "Пари на {0} {1}\n\n{2}".format(
            weekdays[today.timetuple().tm_wday],
            today.strftime("%d.%m.%y"),
            response_text)
    while today.timetuple().tm_wday < 4:
        today = today.replace(day=today.day+1)
        if today.isoformat() in curriculum and today.timetuple().tm_wday < 5:
            curri = "\n\n".join(curriculum[today.isoformat()])
            response_text = "{0}\n\n\nПари на {1} {2}\n\n{3}".format(
                response_text,
                weekdays[today.timetuple().tm_wday],
                today.strftime("%d.%m.%y"),
                curri)
        else:
            response_text = "{0}\n\n\nПари на {1} {2}\n\n{3}".format(
                response_text,
                weekdays[today.timetuple().tm_wday],
                today.strftime("%d.%m.%y"),
                "В цей день пар немає")
    messages = response_text.split('\n\n\n')
    for message in messages:
        response_msg = json.dumps(
            {
                "recipient": {"id": fbid},
                "message": {
                    "text": message,
                    "quick_replies": [
                        {
                            "content_type": "text",
                            "title": "На сьогодні",
                            "payload": "PAYLOAD_TODAY"
                        },
                        {
                            "content_type": "text",
                            "title": "На завтра",
                            "payload": "PAYLOAD_NEXTDAY"
                        },
                        {
                            "content_type": "text",
                            "title": "На цей тиждень",
                            "payload": "PAYLOAD_WEEK"
                        },
                        {
                            "content_type": "text",
                            "title": "На наступний тиждень",
                            "payload": "PAYLOAD_NEXTWEEK"
                        }
                    ]
                }
            }
        )
        status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
        pprint(status.json())


class MessengerBot(generic.View):

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == settings.MESSENGER_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse("Error, invalid token")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incomming_message = json.loads(self.request.body.decode('utf-8'))
        pprint(incomming_message)
        for entry in incomming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    #pprint(message)
                    if 'quick_reply' in message['message']:
                        current_payload = message['message']['quick_reply']['payload']
                        print(current_payload)
                        if current_payload == "PAYLOAD_TODAY":
                            post_today(message['sender']['id'])
                            #return HttpResponse()
                        elif current_payload == "PAYLOAD_NEXTDAY":
                            post_nextday(message['sender']['id'])
                        elif current_payload == "PAYLOAD_WEEK":
                            post_week(message['sender']['id'])
                        elif current_payload == "PAYLOAD_NEXTWEEK":
                            post_nextweek(message['sender']['id'])
                        else:
                            return HttpResponse()
                    else:
                        post_request(message['sender']['id'])
                else:
                    post_request(message['sender']['id'])

        return HttpResponse()