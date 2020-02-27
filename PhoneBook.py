####################################################################################################################
###                                    Algorithms for Bioinformatics
###                                 ***  class Phone Book              ***    
###
### Test number: 4      Class Number: 3         Date:   17 to 21 February 2020
###
### Group
### Student: Bruno Pinto               Number: 201603939
### Student: ....               Number:...
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
        self.list = []
        self.listMail = []
    
    def add_phone(self, name, number, email):
        # complete
        self.list.append({'name' : name, 'number': number})
        self.listMail.append({'name' : name, 'email' : email})
    
    def print_book(self):
        for i in self.list:
            print(i)
    
    def search_by_number(self, number):
        list_search = []
        for i in self.list:
            if i['number'] == number:
                list_search.append(i)
        return list_search

    def search_by_name(self, name):
        list_search = []
        for i in self.list:
            if i['name'] == name:
                list_search.append(i)
        return list_search
    
    def search_by_email(self, email):
        list_search = []
        for i in self.list:
            if i['email'] == email:
                list_search.append(i)
        return list_search
        
    def copy(self):
        pass


if __name__ == "__main__":
    ''' test code here '''
    # complete
    phone = PhoneBook()
    phone.add_phone("Bruno", "91919", "bruno@gjaj.com")
    phone.add_phone("Bruno1", "123", "bruno@gmail.com")
    phone.add_phone("Bruno2", "1234", "pinto@gmail.com")
    phone.add_phone("Bruno", "123", "bruno1k@gmail.com")
    phone.print_book()
    print(phone.search_by_name('Bruno'))
    print(phone.search_by_number('1234'))
    print(phone.search_by_email('bruno@gmail.com'))
    
    