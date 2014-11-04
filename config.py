from fwiki import app

#Should we run in debug mode?
app.config['debug'] = True

#The title of the wiki
app.config['title'] = 'FWiki'

#The wiki logo
app.config['logo_file'] = 'logo.png'

#Sets wether "Powered by ..." should appear in the footer
app.config['expose'] = True

app.config['edit_pass'] = '1234'

#Database options
app.config['db_name'] = 'wiki.db'
app.config['db_err_title'] = 'Interal Error'
app.config['db_err_msg'] = 'An interal error occurred'
