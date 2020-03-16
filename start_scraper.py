import main

folder_path = '/Users/jerryfanelli/Desktop/DSBA/Second Semester/Marketing/Group/'
database_name = 'percy_jackson.db'

url = 'https://www.amazon.it/mare-mostri-Percy-Jackson-dellOlimpo/product-reviews/8804603569/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
start_page = 1
end_page = 5

main.main(folder_path, database_name, url, start_page, end_page)
