import requests
import datetime
import pytz
import json
import os.path
from os import chmod

from time import sleep # функция для создания паузы в выполнении программы
import talk2telegramapi # модуль с функциями общения с API Telegram
import fiitinfo  # Модуль с информацией по группе Фиит

def w_2_json(source_file, source_list):
	try:
		with open(source_file, 'w', encoding='utf-8') as ID_List:
	  		ID_List.write(json.dumps(source_list, ensure_ascii=False))
	except PermissionError as Err:
		os.chmod(source_list, 664)
		os.chmod(source_list, 0o664)

def read_f_json(source_file):
	#try:
	with open(source_file, 'r', encoding='utf-8') as ID_List:
		source_list = json.load(ID_List)
	"""except PermissionError as Err:
		os.chmod(source_list, 664)
		os.chmod(source_list, 0o664)
	except FileNotFoundError as Err:
		if source_file == 'fiit_dictionary.json':
			fiit_dictionary = {}
			fiit_dictionary.update({'updown':'up'})
			fiit_dictionary.update({'schedule_chat_list':[]})
			fiit_dictionary.update({'send_schedule_bool':False})
			fiit_dictionary.update({'schedule':fiitinfo.schedule_up})
			fiit_dictionary.update({'last_upd_id':1})
			fiit_dictionary.update({'init_week':False})
			w_2_json('fiit_dictionary.json', fiit_dictionary)
			source_list = fiit_dictionary
		if source_list == 'PD_mehmat.json':
			print()#do smth"""
	return source_list

# Функция команды schedule_init
def do_schedule_init(chat_id,fiit_dictionary):
    if chat_id not in fiit_dictionary['schedule_chat_list']:
        fiit_dictionary['schedule_chat_list'].append(chat_id)
        w_2_json('fiit_dictionary.json', fiit_dictionary)
        talk2telegramapi.send_message(chat_id,'Ваш чат добавлен в список рассылки.')
    else:
        talk2telegramapi.send_message(chat_id,'Ваш чат уже есть в списке рассылки.')


# Функция команды schedule_stop
def do_schedule_stop(chat_id, fiit_dictionary):
	if chat_id in fiit_dictionary['schedule_chat_list']:
		fiit_dictionary['schedule_chat_list'].remove(chat_id)
		w_2_json('fiit_dictionary.json', fiit_dictionary)
		talk2telegramapi.send_message(chat_id,'Ваш чат удалён из списка рассылки.')
	else:
		talk2telegramapi.send_message(chat_id,'Вашего чата нет в списке рассылки.')



# Функция команды init_up
def do_init_up(chat_id):
    talk2telegramapi.send_message(chat_id,'Теперь неделя верхняя.')
    return fiitinfo.schedule_up, 'up'
    # необходима авторизация изменения верх. ниж. недели


# Функция команды init_down
def do_init_down(chat_id):
    talk2telegramapi.send_message(chat_id,'Теперь неделя нижняя.')
    return fiitinfo.schedule_down, 'down'
    # необходима авторизация изменения верх. ниж. недели



# Задаём словарь информационных команд
dict_of_commands = {
    # Информация о деканате
    '/dean':'Информация о деканате',
    '/dean@FiitRndBot':'Информация о деканате',
    # Информация о дисциплинах
    '/disciplines':'Информация о дисциплинах',
    '/disciplines@FiitRndBot':'Информация о дисциплинах',
    # Информация о сессии
    '/session':'Информация о сессии',
    '/session@FiitRndBot':'Информация о сессии',
    # Спсиок группы с контактами
    '/group_list':"Спсиок группы с контактами",
    '/group_list@FiitRndBot': "Спиcок группы с контактами",
    # Инизиализация  рассылки расписания
    '/schedule_init':'Инизиализация рассылки расписания',
    '/schedule_init@FiitRndBot':'Инизиализация рассылки расписания',
    # Остановка рассылки расписания
    '/schedule_stop':'Остановка рассылки расписания',
    '/schedule_stop@FiitRndBot':'Остановка рассылки расписания',
    # Инициализация верхней недели
    '/init_up':'Инициализация верхней недели',
    '/init_up@FiitRndBot':'Инициализация верхней недели',
    # Инициализация нижней недели
    '/init_down':'Инициализация нижней недели',
    '/init_down@FiitRndBot':'Инициализация нижней недели',
    # Расписание на неделю
    '/schedule_week':'Расписание на эту неделю',
    '/schedule_week@FiitRndBot':'Расписание на эту неделю',
    # Службная команда
    '/vars':'Значения переменных в стандартный вывод',
    '/vars@FiitRndBot':'Значения переменных в стандартный вывод',
}

if os.path.exists('fiit_dictionary.json'):
    fiit_dictionary = read_f_json('fiit_dictionary.json')
    fiit_dictionary['restart_inc'] = fiit_dictionary['restart_inc'] + 1
    w_2_json('fiit_dictionary.json', fiit_dictionary)
    schedule = fiitinfo.schedule_down
else:
    fiit_dictionary = {}
    fiit_dictionary.update({'updown':'up'})
    fiit_dictionary.update({'schedule_chat_list':[]})
    fiit_dictionary.update({'send_schedule_bool':False})
    #fiit_dictionary.update({'schedule':fiitinfo.schedule_up})
    fiit_dictionary.update({'last_upd_id':1})
    fiit_dictionary.update({'init_week':False})
    fiit_dictionary.update({'restart_inc':1})
    schedule = fiitinfo.schedule_down
    w_2_json('fiit_dictionary.json', fiit_dictionary)



# Основная функция содержащая тело бота
def main():
    # Задаём часовой пояс
    servertz = pytz.timezone("Europe/Moscow")

    # Бесконечный цикл бота
    while True:
        #  Меняем значение верхней нижней недели
        fiit_dictionary = read_f_json('fiit_dictionary.json')
        if not fiit_dictionary['init_week']:
            if fiit_dictionary['updown']=='up':
                fiit_dictionary['updown'] = 'down'
                fiit_dictionary['schedule'] = fiitinfo.schedule_down
                fiit_dictionary['init_week'] = True
                schedule = fiitinfo.schedule_down
                w_2_json('fiit_dictionary.json',fiit_dictionary)
            elif fiit_dictionary['updown']=='down':
                fiit_dictionary['updown'] = 'up'
                fiit_dictionary['schedule'] = fiitinfo.schedule_up
                fiit_dictionary['init_week'] = True
                schedule = fiitinfo.schedule_up
                w_2_json('fiit_dictionary.json',fiit_dictionary)
        # Переманная текущего дня и времени по Москве
        now = datetime.datetime.now(servertz)

        # В конце недели меням значения флага инизиализации недели
        if now.weekday() == 6 and now.hour ==23 and now.minute ==59 and now.second >= 55 :
            fiit_dictionary['init_week'] = False
            sleep(10)#Избегаем повторноо переключения недели. Изменение этой перевнной должно быть 1 раз в неделю


        # Получаем последнее сообщенеие
        message = talk2telegramapi.get_last_message()


        # Если список сообщений не пуст тогда делаем всё что в этом if (разбор команды и ответ)
        if message:
            if fiit_dictionary['last_upd_id'] == message['update_id']: #если оно то же самое то переходим к следующей итерации
                sleep(2)
                continue
            else:# Если нет, то обновляем значение последнего update_id и выполняем последующие команды
                fiit_dictionary['last_upd_id'] = message['update_id']
                w_2_json('fiit_dictionary.json', fiit_dictionary)

            # Присваиваем переменным значения из вновь пришедшего сообщения
            msg_text = message['text']
            msg_chat_id = message['chat_id']

            # Переписываем выбор команды

            if msg_text in dict_of_commands :
                # Инизиализация и остановка рассылки расписания
                if (msg_text == '/schedule_init' or msg_text == '/schedule_init@FiitRndBot'):
                    do_schedule_init(msg_chat_id,fiit_dictionary)

                elif (msg_text == '/schedule_stop' or msg_text == '/schedule_stop@FiitRndBot'):
                    do_schedule_stop(msg_chat_id,fiit_dictionary)

                # Инизиализация типа недели
                elif (msg_text == '/init_up' or msg_text == '/init_up@FiitRndBot'):
                    schedule, fiit_dictionary['updown'] = do_init_up(msg_chat_id)
                    fiit_dictionary['updown'] = 'up'
                    w_2_json('fiit_dictionary.json',fiit_dictionary)

                elif (msg_text == '/init_down' or msg_text == '/init_down@FiitRndBot'):
                    schedule, fiit_dictionary['updown'] = do_init_down(msg_chat_id)
                    fiit_dictionary['updown'] = 'down'
                    w_2_json('fiit_dictionary.json',fiit_dictionary)

                #  Отправляем информацию о Деканате
                elif (msg_text == '/dean'  or msg_text =='/dean@FiitRndBot'):
                    talk2telegramapi.send_message(msg_chat_id,fiitinfo.dean_info)

                # Отправляем информацию о Дисциплинах
                elif (msg_text == '/disciplines' or msg_text == '/disciplines@FiitRndBot'):
                    disciplines = ''
                    for i in fiitinfo.disciplines:
                        disciplines += i['name']+'\n'+i['teacher']+'\n'+i['phone']+'\n'+'\n'
                    talk2telegramapi.send_message(msg_chat_id,disciplines)

                # Отправляем информацию о Сессии
                elif (msg_text == '/session' or msg_text == '/session@FiitRndBot'):
                    talk2telegramapi.send_message(msg_chat_id,fiitinfo.session_info)

                # Отправляем список группы
                elif (msg_text == '/group_list' or msg_text == '/group_list@FiitRndBot'):
                    grouplist = ''
                    for i in fiitinfo.students:
                        grouplist += i['firstname']+' '+i['surname']+' '+i['patronymic']+' '+'\n'+i['phone']+'\n'+'Номер в журнале'+i['journal_number']+'\n'+'\n'

                    talk2telegramapi.send_message(msg_chat_id,grouplist)

                elif (msg_text == '/schedule_week' or msg_text == '/schedule_week@FiitRndBot'):
                    schedule_week = ''
                    for i in range(0,5):
                        schedule_week += fiitinfo.week_days[i]+'\n'+ str(schedule[i]) +'\n'+'\n'
                    talk2telegramapi.send_message(msg_chat_id,schedule_week)

                elif (msg_text == '/vars' or msg_text == '/vars@FiitRndBot'):
                    print('schedule_chat_list= ',fiit_dictionary['schedule_chat_list'])
                    print('updown= ',fiit_dictionary['updown'])
                    print('send_schedule_bool= ',fiit_dictionary['send_schedule_bool'])
                    print('schedule= ',schedule)
                    print('Время на сервере ',now)
                else:
                    talk2telegramapi.send_message(msg_chat_id,'Кто-то забыл прописать функцию для команды.')

            else:
                talk2telegramapi.send_message(message['chat_id'],'Не в списке команд')



            # Если текст сообщения stop останавливаем бота
            if msg_text == 'stop':
                talk2telegramapi.send_message(message['chat_id'],"Oh No!... I'am dying...",)
                break






        # Рассылаем расписание в чаты в 9.00 если оно уже не разослано
        if now.weekday() in range(5) and now.hour == 16 and not fiit_dictionary['send_schedule_bool']:
            for i in fiit_dictionary['schedule_chat_list']:
                talk2telegramapi.send_message(i, 'Неделя = '+fiit_dictionary['updown'])
                talk2telegramapi.send_message(i, ','.join(schedule[now.weekday()]))
            fiit_dictionary['send_schedule_bool'] = True
            w_2_json('fiit_dictionary.json',fiit_dictionary)



        # В 23 часу сбрасываем флаг отправки расписания
        if now.weekday() in range(5) and now.hour == 23 and fiit_dictionary['send_schedule_bool']:
            fiit_dictionary['send_schedule_bool'] = False


        # Ждём 1 секунду до следующего запроса
        sleep(1)





if __name__ == '__main__':
    main()
