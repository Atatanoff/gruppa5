
from parser_pages import ParserSearchPage


# уловить ошибку playwright._impl._errors.TimeoutError
# вывести ошибку загрузки страницы
def print_data(data: dict):
    print("#"*124)
    for key, value in data.items():
        print(f"# {key}: {value}".ljust(123)+"#")
    print("#"*124)

def main():
    p = ParserSearchPage(headless=True, verbose=True)
    p.set_search_data(input("Введите ОГРН, ИНН, название, адрес или ФИО\n"))
    p.run()
    print_data( p.ip_indx)
    print_data( p.get_ip_by_number(input("Введите порядковый номер нужного контрагента\n")))
    p.close()

if __name__ == '__main__':
    main()
