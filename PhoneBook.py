####################################################################################################################
###                                    Algorithms for Bioinformatics
###                                 ***  class Phone Book              ***    
###
### Test number: 4      Class Number: 3         Date:   17 to 21 February 2020
###
### Group: 2
### Student: Bruno Pinto               Number: 201603939
### Student: Duarte Melo               Number: 201604476
###
####################################################################################################################
### Complete the code below for the object PhoneBook
### In main give example on how to create, update, insert and use object PhoneBook
### Explain in comments how the data will be organized

class PhoneBook:
    ''' Implements a Phone Book '''
    
    def __init__(self):
        ''' initializes phone book with appropriate data structure '''
        # complete
        self.dict = {}
        self.dictMail = {}
    
    def add_phone(self, name, number):
        # complete
        self.dict[name] = number
    
    def add_mail(self, name, mail):
        # complete
        self.dictMail[name] = mail
    
    def print_book(self):
        print(self.dict)
        print(self.dictMail)


    def search_by_name(self, name):
        return self.dict[name] + " " + self.dictMail[name]
    

    def search_by_number(self, number):
        for x, y in self.dict.items():
            if y == number:
                return x
        return ""

    def search_by_email(self, mail):
        for x, y in self.dictMail.items():
            if y == mail:
                return x
        return ""
        
    def copy(self): 
        deepCopy = PhoneBook()
        deepCopy.dict = {name: number for name, number in self.dict.items()}
        return deepCopy


if __name__ == "__main__":
    ''' test code here '''
    # complete
    phone = PhoneBook()
    phone.add_phone("Bruno", "91919")
    phone.add_phone("Bruno1", "123")
    phone.add_mail("Bruno2", "pinto@gmail.com")
    phone.add_mail("Bruno", "bruno1k@gmail.com")
    phone.print_book()
    print(phone.search_by_name('Bruno'))
    print(phone.search_by_number('123'))
    print(phone.search_by_email('bruno@gmail.com'))
    print(phone.search_by_email('bruno1k@gmail.com'))
    
    