import sys
import os
import pickle
import xbmcvfs
import xbmcaddon

# Database location from plugin info
__addon__       = xbmcaddon.Addon(id='plugin.program.shortlist')
__addondir__    = xbmcvfs.translatePath( __addon__.getAddonInfo('profile') )

# Settings to see which database
__database__	= __addon__.getSetting('database').lower()
databasePath 	= __addondir__ + __database__ + ".db"

# Setting for last used database
__lastused__ = __addon__.getSetting( "lastused" )

def addItem( database, item ):
    # Append item
    # TODO: Check if already in database
    database.append( item )

def addItemToDatabase( dbName, item ):
    # Adds an item to the specified database
    database = getDatabaseByName( dbName )

    # Check if already in database and add
    exists = itemExists( database, item )
    if not exists:
        # Add to database
        database.append( item )

        # Save database again
        saveDatabaseByName( database, dbName )
        return True;

    return False

    # Store as most recently used database

def itemExists( database, item ):
    # Search database end return if item exists based on filename
    for i in database:
        if( i.filename == item.filename ):
            return True;

    return False;

def deleteItem( database, filename ):
    # Delete item based on filename
    for item in database:
        if( item.filename == filename ) :
            database.remove( item )
            break

def deleteItemFromDatabase( dbName, filename ):
    # Delete item based on filename from named database
    database = getDatabaseByName( dbName )
    if database is not None:
        deleteItem( database, filename )
        saveDatabaseByName( database, dbName )

def moveUp( database, filename ):
    # Moves an item earlier in the list
    for i in range(0, len( database ) ):
        item = database[i]
        if item.filename == filename:
            database.remove( item )
            database.insert( i-1, item )

def moveDown( database, filename ):
    # Moves an item later in the list
    for i in range(0, len( database ) ):
        item = database[i]
        if item.filename == filename and i<(len(database)-1):
            database.remove( item )
            database.insert( i+1, item )
            break

def moveToTop( database, filename ):
	# Move an item to the start of the list
	for i in range(0, len( database ) ):
		item = database[i]
		if item.filename == filename and i>0:
			database.remove( item )
			database.insert( 0, item )

def moveToBottom( database, filename ):
	# Move an item to the end of the list
	length = len( database )

	for i in range(0, length - 1 ):
		item = database[i]
		if item.filename == filename and i<(len(database)-1):
			database.remove( item )
			database.insert( length - 1, item )

def getDatabase():
    # Load database if it exists
    database = []
    if os.path.exists( databasePath ):
        shortlistFile = open( databasePath, 'rb')
        database = pickle.load( shortlistFile )
        shortlistFile.close()

    return database

def getDatabaseByName( dbName ):
    # Get specified database
    database = None
    dbPath = __addondir__ + dbName

    # xbmc.log( dbPath, xbmc.LOGNOTICE);

    if os.path.exists( dbPath ):
        shortlistFile = open( dbPath, 'rb')
        database = pickle.load( shortlistFile )
        shortlistFile.close()

    return database


def saveDatabase( database ):
    # Check folder exists, if not create it
    if not os.path.exists( __addondir__ ):
        os.makedirs( __addondir__ )

    # Open file and save data as python pickle
    databaseFile = open( databasePath , 'wb')
    pickle.dump( database, databaseFile )
    databaseFile.close()

def saveDatabaseByName( database, dbName ):
    # Save a database useding specified name

    # Check folder exists, if not create it
    if not os.path.exists( __addondir__ ):
        os.makedirs( __addondir__ )

    dbPath = __addondir__ + dbName

    # Open file and save data as python pickle
    databaseFile = open( dbPath , 'wb')
    pickle.dump( database, databaseFile )
    databaseFile.close()

def listDatabases():
    # Return a list of available databases

    # Check folder exists, if not create it
    if not os.path.exists( __addondir__ ):
        os.makedirs( __addondir__ )

    lst = os.listdir( __addondir__ )

    # If no databases, create default
    if len( lst ) == 0:
        database = []
        saveDatabaseByName( database, "shortlist.db" )
        lst.append( "shortlist.db" )

    # Blank Database
    dbs = []

    # Add last used

    # Show only database files
    for l in lst:
        if l[-3:] == ".db":
            dbs.append( l[:-3].title() )

    return dbs
