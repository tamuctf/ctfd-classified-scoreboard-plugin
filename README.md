# CTFd-Classified-Scoreboard-Plugin
### V1.0.3 BETA
This is a CTFd platform plugin that enables the scoreboard to show scores by classification.

### *DISCLAIMER*
This plugin does *not* automatically classify competitors based their email domain, so all competitors must be maually classified. To avoid this, you can install the [CTFd-Classify-On-Register](https://github.com/tamuctf/ctfd-classify-on-register-plugin) Plugin.

This plugin will also replace the client-side scoreboard, so please understand that whatever theme you will be using will be overwritten by the scoreboard.html file included with this plugin. My suggestion if you would like to alter the scoreboard page is to alter the scoreboard.html file included with this plugin. 

# Usage:
The Configuration page for this plugin can be found at (IP Address: Port)/admin/plugins/classification/ . In this page you can view a list of all of the users with their scores and classifications. You can also add/change a non-admin's classification in this page.

*Note:*
Administrators are not affected by this plugin, and therefore will not show up in the configuration page.

*Note:*
The leftmost coloumn in the configuration page is the User's ID number, not necessarily

### To add/change a classification for a user:
1. Go to Configuration page
1. Select the user who is desired to add/change a classification for
1. Select either a preconfigured classification or "other"
  * If "Other" is chosen, specify the classification desired. (This is CaseSensative)
1. Click "Submit"

### Client-Side Scoreboard
When the users log into the page and score any points they will be present in the scoreboard in both the "All" category and the category they are assigned to.

*Note:*
Currently, users will only be presented with the scoreboard that corresponds to their classification with TAMUctf specific classifications. Currently, this is planned to be fixed.

Just simply select the classification you'd like to see in the dropdown at the top left of the scoreboard page, and only the users in that category will appear (expect in the case that "All" is select).




