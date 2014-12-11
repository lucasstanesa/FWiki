from fwiki import app

app.config.update({
    'DEBUG'        : True,      #Debug mode
    'title'        : 'FWiki',   #Wiki title
    'pass'         : '1234',    #Janitorial password
    'locked'       : True,      #Password protect article creation and editing
    
    'title_chars'  : 'abcdefghijklmnopqrstuvwxyz12345667890', #characters allowed in article titles

    'db_name'      : 'wiki.db',
    's_db_title'   : 'Internal Error',
    's_db_msg'     : 'An interal error occurred',
    's_lock_title' : 'Locked',
    's_lock_msg'   : 'Article creation and editing are currently disabled'
})

