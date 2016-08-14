# deleteStatic.js

There is way available to course authors to delete the entire static folder in an edX course. Importing a course merges the new and old static folder, but does not delete the old static folder.

`deleteStatic.js` contains two functions that can be used to delete all the files in the course static folder from the developer console (after navigating to Conent --> Files and Uploads). They are:

    1. `deleteSinglePage()`: This deletes a single page (up to 50 assets) from the static folder
    2. `deleteManyPages(numPages)`: This function deletes a single page, waits a while for new assets to load, then deletes the page again, and repeats `numPages` times.   

Use with caution.