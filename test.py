import requests

def read(txt): #чтение из файла
    res = []
    f = open(txt, 'r', encoding='utf-8')
    for line in f:
        a = line.split(',')
        res.append([a[0].strip(), a[1].strip()])
    f.close()
    return res

def test(pairs): # сравнение данных из файла с данными из росреестра; pairs - пара [номер телефона, название оператора]
    res = [0, 0, 0] # 0 - данные верны, 1 - не верны, 2 - не получили ответ / статистика для вывода в консоль
    res_for_file = [] # статистика для вывода в файл
    for pair in pairs:
        r = requests.get('http://rosreestr.subnets.ru/', params = 'get=num&format=json&num=' + pair[0] )
        if r.status_code == 200:
            operator_reestr = r.json()['0']['operator']
            if operator_reestr == pair[1]:
                res_for_file.append([pair[0], pair[1], operator_reestr, '1'])                
                res[0] += 1
            else:
                res_for_file.append([pair[0], pair[1], operator_reestr, '0'])
                res[1] += 1
        elif r.status_code == 404:
            res_for_file.append([pair[0], pair[1], '2'])            
            res[2] += 1
    return res_for_file, res

def write_in_file(file, a): # запись в файл
    f = open(file, 'w', encoding='utf-8')
    for i in a:
        for j in i:    
            f.write(j + ' ')
        f.write('\n')
    f.close()

if __name__ == "__main__":
    (output, stats) = test(read('input'))
    write_in_file('output', output)
    print('correct data = {0}, incorrect data = {1}, no answer = {2}'.format(stats[0], stats[1], stats[2]))    
    print('look for file "output" also')
