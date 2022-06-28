import requests


# TODO: Convert recieved url data to usefull data - price, year

def purify_data(price_string):
    pure_price = price_string.replace(',', '').replace('<b>', '').replace('</b>', '')
    
    if pure_price == '': pure_price = '0'
    
    return int(pure_price)

# TODO: More relaable way to get max page
def get_max_page(string):
    max_page = string.split(' &nbsp;&nbsp; <a name="nav_id" rel="next" class="navi" href="')[0]    
    max_page = max_page.replace('</a>', '')    
    max_page = max_page.replace(' ..', '') 
    max_page = max_page.split('">')[-1]
    
    try:
        max_page = int(max_page)
    except Exception as e:
        max_page = 0
        
    return max_page


output_data = {}
def run(page):
    # TODO: Create user input
    search_make = 'bmw'
    search_model = '330'
    url = f'https://www.ss.lv/lv/transport/cars/{search_make}/{search_model}/sell/page{page}.html'

    response = requests.get(url=url)
    html_string = response.text

    max_pages = get_max_page(html_string)
    raw_rows = html_string.split('  €</td>')

    raw_rows[-1] = ''
    global output_data
    for raw_row in raw_rows[:-1]:
        column_split = raw_row.split('nowrap c=1>')
        raw_year = column_split[-4].replace('</td><td class="msga2-o pp6"', '')
        year = purify_data(raw_year)
        price = purify_data(column_split[-1])

        if year not in output_data:
            output_data[year] = [price]
        else:
            if price not in output_data[year]:
                output_data[year].append(price)
                
    if page < max_pages:
        run(page+1)
    
def get_average(data):
    keys = list(data)
    keys.sort()
    
    for year in keys:
        print(f'    Year - {year} ({len(data[year])})') 
        print(f'Min: {min(data[year])}')
        print(f'Max: {max(data[year])}')
        print(f'Avg: {round(sum(data[year]) / len(data[year]))}')
        print()
            
    
    
run(1)

get_average(output_data)