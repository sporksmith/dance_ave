dance-ave
=========

The telephony back-end for [Dance Ave](http://www.cityofplay.org/traf/) a live-action dancing game.

Setup
=====

Django setup
------------

This game is implemented as a [Django](https://www.djangoproject.com/) module.
To set it up, add `dance_ave` to your Django `INSTALLED_APPS`, and include `dance_ave.urls` in your `urlpattern`s.
You'll probably also want to enable the Django admin site, which we use for authentication and managing
the song stations.
e.g.:

    urlpatterns = patterns('',
        ...
        url(r'^dance_ave/', include('dance_ave.urls')),
        ...
        url(r'^admin/', include(admin.site.urls)),
        ...
        )
      
Tropo setup
-----------

Dance Ave uses [Tropo](https://www.tropo.com/) for its telephony services.
You'll need to create an account and point it at the Dance Ave `home` URL.

Game setup
----------

You'll need to create some song stations.
Use the Django admin interface, pointing each song station at some audio file
URL that Tropo will be able to access.

Running the game
================

You can monitor the running game from the `dashboard` view.
This will show you the players who have called so far, and how many
stations they have completed.
You can reset the game (deleting all player data) by checking the
"are you sure" boxes and hitting the `RESET GAME` button.
