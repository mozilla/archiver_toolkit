# How to archive content from mozilla.org 

## 1. Get commit access to website-archive tree in SVN 

* Here is a bug template: <http://mzl.la/1bcLR7d>
* You will need your access to be approved (in the bug) by someone with authority over the content. Jennifer Bertsch, Chris More, or David Boswell can all vouch for you.

## 2. Clone the archiver repository 

If you're reading this README, you're in the right place. Clone this repo:

    git clone https://github.com/hoosteeno/archiver_toolkit.git

## 3. Checkout the website-archive repository 

In the github folder you created in step 2, checkout the SVN folder that contains warchived www.mozilla.org content:

    svn checkout https://svn.mozilla.org/projects/website-archive.mozilla.org/www.mozilla.org

## 4. Put some new content into the SVN repository 

The goal of this effort is to add something to the repository. Use wget to spider a subdirectory of www.mozilla.org. The below command does it exactly right. It contains two parameters you must adjust:

1. `www.mozilla.org/devpreview_releasenotes`: this should adjusted to `www.mozilla.org/some_descriptive_folder_name`
2. `http://www.mozilla.org/projects/devpreview/releasenotes/`: this should adjusted to `http://www.mozilla.org/the_path_to_the_folder_you_are_archiving`

    wget -e robots=off -w 1 --mirror -p --adjust-extension --no-parent \
    --convert-links --no-host-directories -P \
    www.mozilla.org/devpreview_releasenotes \
    http://www.mozilla.org/projects/devpreview/releasenotes/

## 5. Process the HTML you just retrieved 

There are a handful of minor changes we like to make to archived content. We like to get rid of the search tool, since it is not guaranteed to work forever. And we like to add a message at the top of the page explaining that the content is archived. The archiver_toolkit repository contains a python command that processes these files. To run it...

1.(optional) Set up a virtualenv to isolate this repository's libraries from your system libraries: `virtualenv --no-site-packages venv && . venv/bin/activate`
2.Install required libraries: `pip install -r requirements.txt`
3.Run the script -- pass it the path to the new content: `python archive.py www.mozilla.org/some_descriptive_folder_name/`

## 6. Commit your changes 

Now that the content is ready, commit it to the website-archive SVN tree:

    svn add www.mozilla.org/some_descriptive_folder_name
    svn commit

## 7. Redirect the original content to the archives 

... documentation to come ...

## 8. Delete the original content from the www.mozilla.org SVN tree 

... documentation to come ...
