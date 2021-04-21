import sys
import os
import pickle
import xbmc
import xbmcaddon

# Database location from plugin info
__addon__       = xbmcaddon.Addon(id='plugin.program.shortlist')
__addondir__    = xbmc.translatePath( __addon__.getAddonInfo('profile') )

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
