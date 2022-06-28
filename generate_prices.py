import requests, csv
from datetime import datetime


class GeneratePrices():
    page = 1

    def run(self, make, model, file_path):
        # Get price list
        price_list = self.get_prices(make, model)
        
        # Get file full path
        full_path = self.generate_full_file_path(make, model, file_path)
        
        # Generate csv file with prices
        self.generate_csv(price_list, full_path)
    
    def get_prices(self, make, model):  
        output_data = {}
        max_pages = 1
        page = 1
        while page <= max_pages:
            url = f'https://www.ss.lv/lv/transport/cars/{make}/{model}/sell/page{page}.html'
        
            # Get HTML string from url
            response = requests.get(url=url)
            html_string = response.text
            
            # Get url page size
            max_pages = self.get_max_page(html_string)
        
            # Main script of getting prices per year
            raw_rows = html_string.split('  €</td>')
            raw_rows[-1] = ''
            
            for raw_row in raw_rows[:-1]:
                column_split = raw_row.split('nowrap c=1>')
                raw_year = column_split[-4].replace('</td><td class="msga2-o pp6"', '')
                year = self.purify_data(raw_year)
                price = self.purify_data(column_split[-1])

                if year not in output_data:
                    output_data[year] = [price]
                else:
                    if price not in output_data[year]:
                        output_data[year].append(price)

            # Switch to another page
            page += 1
        
        print(page)
        
        # Return list with prices 
        return output_data

    # Clean price string
    def purify_data(self, price_string):
        pure_price = price_string.replace(',', '').replace('<b>', '').replace('</b>', '')
        if pure_price == '': pure_price = '0'
        return int(pure_price)
     
    # Get last page number   
    def get_max_page(self, html_string):
        max_page = html_string.split(' &nbsp;&nbsp; <a name="nav_id" rel="next" class="navi" href="')[0]    
        max_page = max_page.replace('</a>', '')    
        max_page = max_page.replace(' ..', '') 
        max_page = max_page.split('">')[-1]
        
        try:
            max_page = int(max_page)
        except Exception as e:
            max_page = 0
            
        return max_page

    # Return full file path
    def generate_full_file_path(self, make, model, filepath):
        filename = f'{make}_{model}_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
        
        full_path = filepath
        if full_path[-1] != '/': full_path += '/'
        full_path += filename
        
        return full_path
    
    # Generate csv file with pricelists
    def generate_csv(self, price_list, full_path):
        # Create new file
        f = open(full_path, 'w')
        
        # Define csv writer
        csv_writer = csv.writer(f)
        
        # Sort years
        years = list(price_list)
        years.sort()
        
        # Insert header
        header = ['Gads', 'Cenas']
        csv_writer.writerow(header)
        
        # Data into file
        for year in years:
            # First column will contain year
            row_data = [year]

            # All other columns will contain prices
            for price in price_list[year]:
                row_data.append(price)
             
            # Write data to csv   
            csv_writer.writerow(row_data)
        
        # Close file
        f.close()