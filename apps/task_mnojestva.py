#Задание «Наводим порядок: упорядочиваем курсы по продолжительности»

from pprint import pprint

courses = ["Java-разработчик с нуля", "Fullstack-разработчик на Python", "Python-разработчик с нуля", "Frontend-разработчик с нуля"]
mentors = [
	["Филипп Воронов", "Анна Юшина", "Иван Бочаров", "Анатолий Корсаков", "Юрий Пеньков", "Илья Сухачев", "Иван Маркитан", "Ринат Бибиков", "Вадим Ерошевичев", "Тимур Сейсембаев", "Максим Батырев", "Никита Шумский", "Алексей Степанов", "Денис Коротков", "Антон Глушков", "Сергей Индюков", "Максим Воронцов", "Евгений Грязнов", "Константин Виролайнен", "Сергей Сердюк", "Павел Дерендяев"],
	["Евгений Шмаргунов", "Олег Булыгин", "Александр Бардин", "Александр Иванов", "Кирилл Табельский", "Александр Ульянцев", "Роман Гордиенко", "Адилет Асканжоев", "Александр Шлейко", "Алена Батицкая", "Денис Ежков", "Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Максим Филипенко", "Елена Никитина"],
	["Евгений Шмаргунов", "Олег Булыгин", "Дмитрий Демидов", "Кирилл Табельский", "Александр Ульянцев", "Александр Бардин", "Александр Иванов", "Антон Солонилин", "Максим Филипенко", "Елена Никитина", "Азамат Искаков", "Роман Гордиенко"],
	["Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Валерий Хаслер", "Татьяна Тен", "Александр Фитискин", "Александр Шлейко", "Алена Батицкая", "Александр Беспоясов", "Денис Ежков", "Николай Лопин", "Михаил Ларченко"]
]
durations = [14, 20, 12, 20]

courses_list = []
for course, mentor, duration in zip(courses, mentors, durations):
	course_dict = {"title":course, "mentors":mentor, "duration":duration}
	courses_list.append(course_dict)

def course_duration(courses_list, durations, courses):
    
	d_durations = {}
	l_data_out = []

	for id, value in enumerate(courses_list):
		
		key = durations[id]  # Получите значение из ключа duration
		d_durations[key,id] = [key,id] # поэтому значение словаря — это список индексов
	
	d_durations = dict(sorted(d_durations.items()))

	for y, z in d_durations.items():
		l_data_out.append(f'{courses[z[1]]} - {z[0]} месяцев')
	return l_data_out
  
pprint(course_duration(courses_list, durations, courses), width=100)



#Задание «Исследуем: есть ли связь между продолжительностью курса и количеством преподавателей»
def connection(mentors, durations, courses):
    
	dur_id = {}
	for id, val in enumerate(courses):
		key = durations[id]
		dur_id[key,id] = [key,id]
		dur_id = dict(sorted(dur_id.items()))

	dur_id_l = []
	for id, val in enumerate(courses):
		
		dur_id_l.append([durations[id],id])
	dur_id_l = list(sorted(dur_id_l))

	list11 = []
	for x1 in range(len(dur_id_l)):
		list11.append(dur_id_l[x1][1])

	nu_men_id = []
	for id, val in enumerate(mentors):
		for num, val1 in enumerate(val):
			x = num
		nu_men_id.append([x,id])
		
	nu_men_id = list(sorted(nu_men_id))

	list12 = []
	for x1 in range(len(nu_men_id)):
		list12.append(nu_men_id[x1][1])

	d_dict = {}
	if list11==list12 :
		d_dict.setdefault("Связь есть", [list11, list12])
		return d_dict
	else:
		d_dict.setdefault("Связи нет", [list11, list12])
		return d_dict

print(connection(mentors, durations, courses))


#Задание «Узнайте топ-3 популярных имён»
def top_3(mentors):
    
    all_list = []
    for m in mentors:
        all_list.extend(m)

    all_names_list = []

    for mentor in all_list:
        name1 = mentor.split()
        name=name1[0]
        all_names_list.append(name)

    unique_names = set(all_names_list)
    unique_names1 = list(unique_names)

    popular = []
    for name in unique_names1:
        popular.append([name, all_names_list.count(name)])

    popular.sort(key=lambda x:x[1], reverse=True)
    top_3 = popular[:3]
    #print(top_3)
    d_top3 = {}
    
    for i in top_3:
        d_top3.setdefault(i[0], f'{i[1]} раз(а)')
    return d_top3

print(top_3(mentors))