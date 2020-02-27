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
    
    def __init__(self, dict={}):
        ''' initializes phone book with appropriate data structure '''
        # complete
        self.dict = dict
    
    def add_phone(self, name, number):
        # complete
        self.dict[name] = number
    
    def print_book(self):
            print(self.dict)
    
    def search_by_number(self, number):
        for name, num in self.dict.items():
            if(num == number):
                return name
        return none

    def search_by_name(self, name):
        return self.dict[name]
        
    def copy(self): 
        deepCopy = PhoneBook()
        deepCopy.dict = {name: number for name, number in self.dict.items()}
        return deepCopy

if __name__ == "__main__":
    ''' test code here '''
    # complete
    phone = PhoneBook()
    phone.add_phone("Bruno", "91919")
    phone.add_phone("Duarte", "123")
    phone.add_phone("Pedro", "1234")
    phone.add_phone("Joao", "123")
    phone.print_book()
    print(phone.search_by_name('Bruno'))
    print(phone.search_by_number('1234'))
    phone2 = phone.copy()
    phone.add_phone("Marta", "1456")
    phone2.add_phone("Joana", "1456")
    phone.print_book()
    phone2.print_book()
    
    