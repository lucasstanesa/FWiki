from fwiki import app

#Should we run in debug mode?
app.config['debug'] = True

#The title of the wiki
app.config['title'] = ''

#The wiki logo
app.config['logo_file'] = None

#Sets if "Powered by ..." appears in the footer
app.config['expose'] = True

#Password required to edit articles
app.config['edit_pass'] = '1234'

#Database options
app.config['db_name'] = 'wiki.db'
app.config['db_err_title'] = 'Interal Error'
app.config['db_err_msg'] = 'An interal error occurred'
