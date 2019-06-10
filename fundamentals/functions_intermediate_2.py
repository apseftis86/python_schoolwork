x = [ [5,2,3], [10,8,9] ] 
students = [
     {'first_name':  'Michael', 'last_name' : 'Jordan'},
     {'first_name' : 'John', 'last_name' : 'Rosales'}
]
sports_directory = {
    'basketball' : ['Kobe', 'Jordan', 'James', 'Curry'],
    'soccer' : ['Messi', 'Ronaldo', 'Rooney']
}
z = [ {'x': 10, 'y': 20} ]


x[1][0] = 15

students[0]['last_name'] = 'Bryant'

sports_directory['soccer'][0] = 'Andres'

z[0]['y'] = 30

print(z)
print(sports_directory)
print(students)
print(x)

def iterateDictionary(some_list):
    for x in range(len(some_list)):
        build_student_obj = ''
        for key, value in some_list[x].items():
              if key == 'first_name':
                  build_student_obj += key + ' - ' + value + ', '
              else:
                  build_student_obj += key + ' - ' + value
        print(build_student_obj)
        
students = [
         {'first_name':  'Michael', 'last_name' : 'Jordan'},
         {'first_name' : 'John', 'last_name' : 'Rosales'},
         {'first_name' : 'Mark', 'last_name' : 'Guillen'},
         {'first_name' : 'KB', 'last_name' : 'Tonel'}
    ]
iterateDictionary(students) 


def iterateDictionary2(key_name, some_list):
    for x in range(len(some_list)):
        for key, value in some_list[x].items():
            if key == key_name:
                print(value)


iterateDictionary2('first_name', students) 
iterateDictionary2('last_name', students)

def printInfo(some_dict):
    for key, value in some_dict.items():
        print(len(value), key.upper())
        for x in range(len(value)):
            print(value[x])
        

dojo = {
   'locations': ['San Jose', 'Seattle', 'Dallas', 'Chicago', 'Tulsa', 'DC', 'Burbank'],
   'instructors': ['Michael', 'Amy', 'Eduardo', 'Josh', 'Graham', 'Patrick', 'Minh', 'Devon']
}

print(printInfo(dojo))
