import requests
import time
import datetime

current_date = datetime.datetime.today()  # Получение сегодняшнего дня

current_date_string = current_date.strftime('%Y-%m-%d 00:00')  # Перевод сегодняшнего дня в str
past_date = datetime.datetime.today() - datetime.timedelta(days=1)  # Получение предыдущего дня
past_date_string = past_date.strftime('%Y-%m-%d 00:00')  # Перевод предыдущего дня в str
past_date_telegram = past_date.strftime('%d.%m.%Y')  # Перевод предыдущего дня в str для telegram


def take_all_chats():
    token = token_usedesk
    offset = 0
    all_tickets = []

    while offset < 20:
        responce = requests.get('https://api.usedesk.ru/tickets',
                                params={
                                    'api_token': token,
                                    'updated_before': current_date_string,
                                    'updated_after': past_date_string,
                                    'fstatus': '3',
                                    'fchannel': '25222',
                                    'offset': offset
                                })
        data = responce.json()
        offset += 1
        all_tickets.extend(data)
        time.sleep(1)

    values_per_key = {}

    for d in all_tickets:
        for k, v in d.items():
            if k == "assignee_id":
                if not values_per_key.get(v):
                    values_per_key[v] = 1
                else:
                    values_per_key[v] += 1  # Создало словарь agent_id: кол-во чатов

    replacemenets = {182004: 'Анастасия', 182870: 'Анастасия Л.', 176964: 'Артем', 186124: 'Артур', 184839: 'Валентина',
                     186484: 'Валерия', 181999: 'Владислав', 187229: 'Дария', 186486: 'Дарья', 182239: 'Екатерина',
                     186488: 'Екатерина П.', 186483: 'Елизавета', 187732: 'Людмила', 186485: 'Маргарита',
                     184335: 'Марина', 184002: 'Мария', 182753: 'Ольга', 182869: 'Ольга М.', 182007: 'Софья',
                     182008: 'Татьяна', 182005: 'Юлия'}

    for i in list(values_per_key):
        if i in replacemenets:
            values_per_key[replacemenets[i]] = values_per_key.pop(i)  # Поменяло agent_id на имена агентов.

    return values_per_key  # Вернули не сортированный словарь values_per_key


result_agent_not_sorted = take_all_chats()  # Присвоили результат выполнения первой функции


def sort_rate():
    return [(k, result_agent_not_sorted[k]) for k in
            sorted(result_agent_not_sorted, key=result_agent_not_sorted.get, reverse=True)]  # Поменяло
    # agent_id на имена агентов.


result_agent_sorted = dict(sort_rate())  # Присвоили результат выполнения второй функции (сортировка)


def rate_without_sum():
    return "\n".join([str(i[0]) + ": " + str(i[1]) for i in result_agent_sorted.items()])  # Передали словарь, как
    # строку


rate_agents_without_sum = rate_without_sum()  # Присвоили результат выполнения третьей функции (словарь в строку


# через join)


def sum_chats():
    return sum(result_agent_not_sorted.values())


sum_agents_chats = sum_chats()


def send_telegram(text: str):
    token = token_telegram
    url = "https://api.telegram.org/bot"
    channel_id = channel
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("post_text error")


if __name__ == '__main__':
    send_telegram("Результаты закрытия чатов за " + past_date_telegram + "." + "\n" + "\n" + rate_agents_without_sum +
                  "\n" + "\n" + "Всего закрыто: " + str(sum_agents_chats))
