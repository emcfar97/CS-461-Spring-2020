##############################################################################
##
## CS 461
## Program #2

## Ethan McFarland
## Em463@mail.umkc.edu
##
##############################################################################

import random, math, csv, copy

class Scheduler():

    def __init__(self, times, courses, instructors, rooms, timeslots=None):

        self.times = times
        self.rooms = rooms
        self.courses = courses
        self.instructors = instructors

        if timeslots: 
            self.timeslots = timeslots
        else:
            self.timeslots = []

            for room in rooms:

                for time in times:

                    course = random.choice(courses)
                    instructor = random.choice(instructors)
                    
                    timeslot = Timeslot(room, time, course, instructor)
                    room.timeslots[time] = timeslot
                    self.timeslots.append(timeslot)
        
    def random_state(self):
        
        timeslots = copy.deepcopy(self.timeslots)
        start, end = random.choices([i for i in range(len(timeslots))], k=2)
        property = random.choice([0, 1, 2, 3])

        if property == 0: 
            timeslots[start].course, timeslots[end].course = timeslots[end].course, timeslots[start].course

        elif property == 1: 
            timeslots[start].instructor, timeslots[end].instructor = timeslots[end].instructor, timeslots[start].instructor

        elif property == 2: 
            timeslots[start].room, timeslots[end].room = timeslots[end].room, timeslots[start].room

        elif property == 3: 
            timeslots[start].time, timeslots[end].time = timeslots[end].time, timeslots[start].time

        schedule = Scheduler(self.times, self.courses, self.instructors, self.rooms, timeslots)

        return schedule
    
    def fitness(self, score=0):

        instructors = {
            instructor.name:0 for instructor in self.instructors
            }

        for room in rooms:

            for timeslot in room.timeslots.values():

                instructor = timeslot.instructor
                course = timeslot.course

                score += 3 if instructor.can_teach(course) and instructor.name != 'Staff' else 0
                score += 1 if instructor.name == 'Staff' else 0

                if room.has_capacity(course): 
                    
                    score += 5
                    score += 2 if room.capacity <= (course.enrolled * 2) else 0
            
                instructors[instructor.name] += 1
        
        for courses in instructors.values():
            score -= 5 * (courses - 4) if courses > 4 else 0
        graduate = instructors['Rao'] + instructors['Mitchell']
        non_graduate = instructors['Hare'] + instructors['Bingham']
        score -= 10 if graduate > non_graduate else 0

        for time in self.times:

            instructors = {}
            courses = self.find_all(time=time)
            for course in courses:
                instructor = course.instructor.name
                instructors[instructor] = instructors.get(instructor, 0) + 1
                
            for instructor, courses in instructors.items():

                if instructor != 'Staff':
                    score -= courses * 5 if courses != 1 else 0

        cs_101 = self.find_all(course='CS 101')
        cs_191 = self.find_all(course='CS 191')
        for course in cs_101:

            time = course.time
            for course_ in cs_191:

                if time == course_.time:

                    score -= 15

                elif time - course_.time == 1:

                    score += 5
                    if course.room == course_.room: 
                        score += 5
                    elif not (course.room == 'Katz' and course_.room == 'Katz'):
                        score -= 3
                    elif not (course.room == 'Bloch' and course_.room == 'Bloch'):
                        score -= 3
                    elif (course.room == 'Bloch' and course_.room == 'Katz') or (course.room == 'Katz' and course_.room == 'Bloch'):
                        score -= 6
 
        cs_201 = self.find_all(course='CS 201')
        cs_291 = self.find_all(course='CS 291')
        for course in cs_201:
    
            time = course.time
            for course_ in cs_291:

                if time == course_.time:

                    score -= 15

                elif time - course_.time == 1:

                    score += 5
                    if course.room == course_.room: 
                        score += 5
                    elif not (course.room == 'Katz' and course_.room == 'Katz'):
                        score -= 3
                    elif not (course.room == 'Bloch' and course_.room == 'Bloch'):
                        score -= 3
                    elif (course.room == 'Bloch' and course_.room == 'Katz') or (course.room == 'Katz' and course_.room == 'Bloch'):
                        score -= 6
        
        return score

    def find_all(self, **kwargs):

        if 'course' in kwargs:

            return [
                timeslot for timeslot in self.timeslots
                if timeslot.course == kwargs['course']
                ]
        
        if 'time' in kwargs:
            
            return [
                timeslot for timeslot in self.timeslots
                if timeslot.time == kwargs['time']
                ]

    def output(self):

        with open('Class Schedule.csv', 'w', newline='') as file:

            writer = csv.writer(file, delimiter=',')
            
            for time in self.times:
                
                line = [time] + [timeslot for timeslot in self.find_all(time=time)]
                writer.writerow(line)

class Timeslot():

    def __init__(self, room, time, course, instructor):

        self.room = room
        self.time = time
        self.course = course
        self.instructor = instructor

    def __repr__(self):

        return f'{self.room}\n{self.course}\n{self.instructor}'

    def __hash__(self): return self.time
    
    def __sub__(self, other): 
        
        return 12 - abs(self.time.hour - other.time.hour)

class Course():
    
    def __init__(self, course, enrolled, section=''): 

        self.course = course
        self.enrolled =  enrolled
        self.section = section
    
    def __repr__(self): return f'{self.course}{self.section} ({self.enrolled})'

    def __eq__(self, other):

        return self.course == other

class Instructor():
    
    def __init__(self, name, courses):

        self.name = name
        self.courses = courses

    def __repr__(self): return f'{self.name}'

    def can_teach(self, course):

        return course in self.courses

class Room():
    
    def __init__(self, room, capacity):

        self.building, self.room = room.split()
        self.capacity = capacity
        self.timeslots = {
            Time('10A'): None, 
            Time('11A'): None, 
            Time('12P'): None, 
            Time('1P'): None, 
            Time('2P'): None, 
            Time('3P'): None, 
            Time('4P'): None
            }

    def __repr__(self): return f'{self.building} {self.room} ({self.capacity})'

    def has_capacity(self, course): return course.enrolled <= self.capacity

    def available(self, time): return time in self.timeslots

class Time():

    def __init__(self, time):

        self.hour = int(time[:-1])
        self.meridian = time[-1:]

    def __repr__(self): return f'{self.hour}{self.meridian}'

    def __hash__(self): return hash(self.__repr__())
    
    def __eq__(self, other):
        
        try:
            return self.hour == other.hour and self.meridian == other.meridian
        except AttributeError:
            return self.__repr__() == other
            
    def __sub__(self, other): 
        
        return 12 - abs(self.hour - other.hour)

courses = [
    Course('CS 101', 40, 'A'),
    Course('CS 101', 25, 'B'),
    Course('CS 201', 30, 'A'),
    Course('CS 201', 30, 'B'),
    Course('CS 191', 60, 'A'),
    Course('CS 191', 20, 'B'),
    Course('CS 291', 20, 'A'),
    Course('CS 291', 40, 'B'),
    Course('CS 303', 50),
    Course('CS 341', 40),
    Course('CS 449', 55),
    Course('CS 461', 40),
    ]
instructors = [
    Instructor(
        'Hare', [courses[0], courses[1], courses[2], courses[3], courses[6], courses[7], courses[8], courses[10], courses[11]]
        ),
    Instructor(
        'Bingham', [courses[0], courses[1], courses[2], courses[3], courses[4], courses[7], courses[6], courses[7], courses[10]]
        ),
    Instructor(
        'Kuhail', [courses[8], courses[9]]
        ),
    Instructor(
        'Mitchell', [courses[4], courses[5], courses[6], courses[7], courses[8], courses[9]]
        ),
    Instructor(
        'Rao', [courses[6], courses[7], courses[8], courses[9], courses[11]]
        ),
    Instructor(
        'Staff', courses.copy()
        )
    ]
times = [
    Time('10A'), 
    Time('11A'), 
    Time('12P'), 
    Time('1P'), 
    Time('2P'), 
    Time('3P'), 
    Time('4P')
    ]
rooms = [
    Room('Haag 301', 70),
    Room('Haag 206', 30),
    Room('Royall 204', 70),
    Room('Katz 209', 50),
    Room('Flarsheim 310', 80),
    Room('Flarsheim 260', 25),
    Room('Bloch 0009', 30)
    ]

T = 1
alpha = 0.9
attempts = changes = 0
schedule = Scheduler(times, courses, instructors, rooms)
schedule.output()

while attempts < 4000:

    attempts += 1
    new_schedule = schedule.random_state()
    delta = new_schedule.fitness() - schedule.fitness()

    if (delta < 0 or (math.exp(-delta / T) >= random.uniform(0, 1))):
        schedule = new_schedule
        changes += 1

    if attempts == 4000 and changes == 400:
        T = alpha * T
        attempts = changes = 0
    
    elif attempts == 4000 and changes == 0:

        schedule.output()
        break

schedule.output()