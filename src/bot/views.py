from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
import requests
import json
import re
import collections

from datetime import date, datetime, timedelta

import telebot
from telebot import apihelper

from pygooglechart import Chart, Axis
from pygooglechart import SimpleLineChart

from bot.models import Rates


# have use proxy cause connection issue
apihelper.proxy = {
    'SOCKS5': '91.238.137.108'
}

bot = telebot.AsyncTeleBot(settings.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(
		message.chat.id,
		'/list, /lst - returns list of all available rates\n\
		/exchange 10 USD to CAD - converts to the second currency\n\
		/history USD/CAD -  shows the exchange rate history'
		)


@bot.message_handler(commands=['list', 'lst'])
def currency_list(message):
	try:
		if Rates.objects.all().exists():
			timestamp = Rates.objects.latest('timestamp').timestamp
			now =  timezone.make_aware(datetime.now(), timezone.get_default_timezone())
			delta = (now - timestamp) > timedelta(minutes=10)
			if delta:
				data = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
				Rates.objects.create(data=data.json())
				data = data.json()['rates']
				reply = ''
				for i in data:
					reply += '● ' + i + ': ' + str(round(data[i], 2))+ '\n'
				bot.send_message(message.chat.id, reply)
			else:
				data = Rates.objects.latest('timestamp').data
				data = data['rates']
				reply = ''
				for i in data:
					reply += '● ' + i + ': ' + str(round(data[i], 2))+ '\n'
				bot.send_message(message.chat.id, reply)
	except:
		bot.send_message(message.chat.id, 'Something went wrong.')


@bot.message_handler(regexp=(r'^/exchange\s([0-9]*\.?[0-9]+\s[a-zA-Z]{3})\sto\s[a-zA-Z]{3}$'))
def exchange(message):
	try:
		splitted_text = message.text.split(' to')
		base_amount = float(re.search(r'[0-9]*\.?[0-9]+', splitted_text[0]).group())
		base = re.search(r'\s[a-zA-Z]{3}', splitted_text[0]).group().upper().strip()
		symbols = re.search(r'\s[a-zA-Z]{3}', splitted_text[1]).group().upper().strip()
		data = requests.get(
			'https://api.exchangeratesapi.io/latest?&base='+base+'&symbols='+symbols
		)
		rate = float(data.json()['rates'][symbols])
		amount = round(base_amount * rate, 2)
		bot.send_message(message.chat.id, 'Ex.: '+str(amount))
	except:
		bot.send_message(message.chat.id, 'Something went wrong.')


@bot.message_handler(regexp=(r'^/history\s[a-zA-Z]{3}/[a-zA-Z]{3}$'))
def history(message):
	try:
		splitted_text = re.search(r'[a-zA-Z]{3}/[a-zA-Z]{3}', message.text).group().split('/')
		base = splitted_text[0].upper()
		symbols = splitted_text[1].upper()
		start = str(date.today() - timedelta(days=7))
		end = str(date.today())
		data = requests.get(
			'https://api.exchangeratesapi.io/history?start_at='+start+'&end_at='+end+'&base='+base+'&symbols='+symbols
		)
		data = data.json()
		chart = SimpleLineChart(700, 400)
		
		chart_data = []
		# using collections.OrderedDict to sort incoming data
		for i in collections.OrderedDict(sorted(data['rates'].items())):
			chart_data.append(round(data['rates'][i][symbols], 2))
		chart.add_data(chart_data)
		print(collections.OrderedDict(sorted(data['rates'].items())))
		# Set the line colour
		chart.set_colours(['0000FF'])
		left_axis= list(
			range(
				round(min(chart_data)),
				round(max(chart_data)+1),
				round(sum(chart_data)/len(chart_data))
			)
		)
		chart.set_axis_labels(Axis.LEFT, left_axis)

		x_labels = []
		# using collections.OrderedDict to sort incoming data
		for i in collections.OrderedDict(sorted(data['rates'].items())):
			x_labels.append(i)
		chart.set_axis_labels(Axis.BOTTOM, x_labels)
		print(chart.get_url())
		bot.send_photo(message.chat.id, chart.get_url())
	except:
		bot.send_message(message.chat.id, 'No exchange rate data is available for the selected currency.')

bot.polling()