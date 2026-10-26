#self : self is very important
#self : connects  oject to class
#self : means current object
#self stores data inside object
#we can any name instead of self
class Student:
    def studentDetails(self):
        print(self)
        
s = Student()
s.studentDetails()

print(s)
# output: it prints self and object same address