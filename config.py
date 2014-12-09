from fwiki import app

app.config.update(
    'DEBUG'        = True,      #Debug mode
    'title'        = 'FWiki',   #Wiki title
    'logo_file'    = None,      #Wiki logo, string filename or None for no logo
    'expose'       = True,      #Print "Powered by..." in the footer?
    'pass'         = '1234',    #Janitorial password
    'locked'       = True,      #Password protect article creation and editing
    
    'db_name'      = 'wiki.db',
    's_db_title'   = 'Internal Error',
    's_db_msg'     = 'An interal error occurred',
    's_lock_title' = 'Locked',
    's_lock_msg'   = 'Article creation and editing are currently disabled'
)

