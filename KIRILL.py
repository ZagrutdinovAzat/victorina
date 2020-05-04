from flask import Flask, request
import json
import random
import wikipedia  # нужно скачать

app = Flask(__name__)

questions = {'Москва': 'Какой город является столицей России?',
             'Рим': 'Этот город был разграблен войсками Карла V в 1527 году. Назовите его.',
             'Будапешт': 'Этот город в Венгрии был образован в результате слияния 3-х городов в 1873. Сможете назвать его?',
             'Дербент': 'Самый старый город Росии населенный уже около 5 тыс. лет.',
             'Иерихон': 'Самый древний город в мире, существующим в настоящее время, появившийся еще в медном веке, а это 9000 лет до н.э.',
             'Пятигорск': 'Город, который в русском жестовом языке можно показать как два пистолета, которые смотрят друг на друга. Это олицетворение дуэли Лермонтова и Мартынова.',
             'Кубер-Педи': 'Австралийский подземный город.',
             'Брест': 'Во Франции и в Беларуси есть города с одинаковым названием. Любопытно, что их освободили от нацистов в один день — 28 июля 1944 года. Что это за города?',
             'Рим': 'Первый город, численность населения которого достигла миллиона?',
             'Мурманск': 'Самым крупным городом России и всего мира из числа расположенных за Полярным кругом является...',
             'Шанхай': 'Самый густо населенный город в мире это?',
             'Оймякон': 'Самый холодный город в мире - ... он же Полюс холода, а также самое холодное место на Земле, где есть постоянное население.'}

correct = ['Правильно! Попробуйте ответить на следующий вопрос:', 'Это правильный ответ! Давайте дальше:',
           'Верно! Следующий вопрос:', 'Вы правы! Попробуйте ответить на следующий вопрос:',
           'В точку! Но дальше сложнее:']
incorrect = ['Это неправильный ответ. Попробуйте ответить на следующий вопрос:',
             'К сожалению, неверно. Попробуйте ответить на следующий вопрос:',
             'Увы, но нет. Уверена, теперь вы справитесь:',
             'Нет, неверно. Может, ответите на следующий вопрос:']

cities = ['Оймякон', 'Шанхай', 'Мурманск', 'Рим', 'Брест', 'Москва', 'Будапешт', 'Берлин', 'Казань', 'Милан', 'Мадрид',
          'Амстердам', 'Дербент', 'Иерихон', 'Пятигорск', 'Кубер-Педи']

sessionStorage = {}

cities_card = {  # id изображений
    'Шанхай': ['1030494/75facfdcedac7260270f'],
    'Оймякон': ['1521359/84f338eb95693145143c'],
    'Мурманск': ['213044/09ed86eeb1f132e46057'],
    'Рим': ['1521359/9cfc48bdb356368328fa'],
    'Брест': ['1030494/c3b9b129d828d6c8ff29'],
    'Москва': ['965417/95ae49ddc16f394de5bb'],
    'Будапешт': ['1521359/40ee5acb48cf968ce554'],
    'Дербент': ['965417/9966b500da95a52bfa4a'],
    'Иерихон': ['213044/c67d240f0f34d61b9b06'],
    'Пятигорск': ['213044/2094da80cb1f9c58b274'],
    'Кибер-Педи': ['1030494/a656857e9c6767c5a01a']
}


@app.route('/post', methods=['POST'])
def main():
    global q
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    dialog(response, request.json)
    return json.dumps(response)


def dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Добро пожаловать в игру! Напишите "Начать" для начала игры'
        res['response']['buttons'] = [{'title': 'Начать', 'hide': True}]
        sessionStorage[user_id] = {
            'game_started': False,
            'count': 0
        }

    elif sessionStorage[user_id]['game_started']:
        if req['request']['command'].capitalize() not in sessionStorage[user_id]['answers']:
            res['response'][
                'text'] = f'''Кажется, такого ответа нет в списке. Выберите один из предложенных ответов.\n\n
                                            {sessionStorage[user_id]["question"]}'''
            res['response']['buttons'] = [{'title': f'{ans}', 'hide': True} for ans in
                                          sessionStorage[user_id]['answers']]
        elif req['request']['command'].capitalize() != sessionStorage[user_id]['answer']:
            question, answer, answers = generate_question(questions)
            sessionStorage[user_id]['count'] += 1
            sessionStorage[user_id]['question'] = question
            sessionStorage[user_id]['answer'] = answer
            sessionStorage[user_id]['answers'] = answers
            res['response']['text'] = f'''{random.choice(incorrect)}\n\n
                                            {sessionStorage[user_id]["question"]}'''

            res['response']['buttons'] = [{'title': f'{ans}', 'hide': True} for ans in
                                          sessionStorage[user_id]['answers']]
        else:
            question, answer, answers = generate_question(questions)
            sessionStorage[user_id]['count'] += 1
            sessionStorage[user_id]['question'] = question
            sessionStorage[user_id]['answer'] = answer
            sessionStorage[user_id]['answers'] = answers

            # изображение
            # res['response']['card'] = {}
            # res['response']['card']['type'] = 'BigImage'
            # res['response']['card']['image_id'] = cities_card[answer]

            res['response']['text'] = f'''{random.choice(correct)}\n\n
                                            {sessionStorage[user_id]["question"]}'''

            res['response']['buttons'] = [{'title': f'{ans}', 'hide': True} for ans in
                                          sessionStorage[user_id]['answers']]

    elif sessionStorage[user_id]['game_started'] is False and req['request']['command'].lower() == 'начать':
        sessionStorage[user_id]['game_started'] = True
        question, answer, answers = generate_question(questions)
        res['response']['text'] = question
        sessionStorage[user_id]['count'] += 1
        sessionStorage[user_id]['question'] = question
        sessionStorage[user_id]['answer'] = answer
        sessionStorage[user_id]['answers'] = answers
        res['response']['buttons'] = [{'title': f'{ans}', 'hide': True} for ans in sessionStorage[user_id]['answers']]
    else:
        res['response']['text'] = 'Жду, когда вы напишите "Начать" для начала игры'
        res['response']['buttons'] = [{'title': 'Начать', 'hide': True}]


def generate_question(quests):
    answer = random.choice(list(quests.keys()))
    answers = []
    city = random.choice(cities)
    while len(answers) < 3:
        while city in answers or city == answer:
            city = random.choice(cities)
        answers.append(city)
    answers.insert(random.randint(0, 3), answer)
    question = f'{quests[answer]}\n\n1) {answers[0]}\n2) {answers[1]}\n3) {answers[2]}\n4) {answers[3]}'
    return question, answer, answers


if __name__ == '__main__':
    app.run()
