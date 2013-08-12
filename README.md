# How to archive content from mozilla.org 

### 1. Get commit access to the necessary source trees in SVN 

* If you are not already a Mozilla committer, you will need to go through the standard commit process: <http://www.mozilla.org/hacking/committer/>
* Then you can file a bug to get access to the website-archive tree. Here is a bug template: <http://mzl.la/1bcLR7d>
* You will need your access to be approved (in the bug) by someone with authority over the content. Jennifer Bertsch, Chris More, or David Boswell can all vouch for you.

If you intend to also delete this content from its original location (see the last step), file a bug to get access to the mozilla.org/mozilla.com SVN trees. Here is a bug template: <http://mzl.la/17JeXr4>

### 2. Clone the archiver repository 

If you're reading this README, you're in the right place. Clone this repo:

    git clone https://github.com/hoosteeno/archiver_toolkit.git

### 3. Checkout the website-archive SVN tree 

In the github folder you created in step 2, checkout the SVN folder that contains archived www.mozilla.org content:

    svn checkout https://svn.mozilla.org/projects/website-archive.mozilla.org/www.mozilla.org

### 4. Put some new content into the SVN tree 

The goal of this effort is to add something to the website-archive SVN tree. Use wget to spider a subdirectory of www.mozilla.org. The below command does it exactly right. It contains two parameters you must adjust:

* `www.mozilla.org/devpreview_releasenotes` should be adjusted to `www.mozilla.org/some_descriptive_folder_name`
* `http://www.mozilla.org/projects/devpreview/releasenotes/` should be adjusted to `http://www.mozilla.org/the_path_to_the_folder_you_are_archiving`

        wget -e robots=off -w 1 --mirror -p --adjust-extension --no-parent --convert-links --no-host-directories \
        -P www.mozilla.org/devpreview_releasenotes \
        http://www.mozilla.org/projects/devpreview/releasenotes/

### 5. Process the HTML you just retrieved 

We like to make a handful of minor changes to archived content. We get rid of the search tool, since it is not guaranteed to work forever. And we add a message at the top of the page explaining that the content is archived. The archiver_toolkit repository contains a python command-line tool that processes these files. To run it...

1. (optional) Set up a virtualenv to isolate this repository's libraries from your system libraries: 

        virtualenv --no-site-packages venv && . venv/bin/activate

2. Install required libraries: 
    
        pip install -r requirements.txt

3. Run the script. Pass it the path to the new content:
    
        python process_files.py www.mozilla.org/some_descriptive_folder_name/
    
### 6. Review the processed code

Open the .html files in your local copy of the SVN tree you have downloaded and modified. In Firefox, use the "File->Open" menu to find them and browse them. Some things to look for:

* Does the archival message appear at the top of every page?
* Do links to other local content work?
* Do links to remote content work?
* Do the pages look like their counterparts on the live server (visible images, working layout, etc.)?

### 7. Commit your changes 

Now that the content is ready to be archived, commit it to the website-archive SVN tree:

    svn add www.mozilla.org/some_descriptive_folder_name
    svn commit www.mozilla.org/some_descriptive_folder_name

The changes will be automatically deployed in about 15 minutes. 

### 8. Verify the deploy

Once the automatic deploy from step 6 happens (usually within 15 minutes), visit the new URL and make sure things work as expected. In the example above, the URL will be:

http://website-archive.mozilla.org/www.mozilla.org/devpreview_releasenotes/projects/devpreview/releasenotes/

### 9. Redirect the original content to the archives 

Requests for the archived content at www.mozilla.org should now be redirected to the archival site. This requires changes to the .htaccess file in the Bedrock code repository (see ["How to Contribute"](http://bedrock.readthedocs.org/en/latest/contribute.html)). If you are not comfortable with this step, you can open a new bug for this change.

1. Clone the [Bedrock code repository](https://github.com/mozilla/bedrock/)
2. Change the etc/httpd/global.conf file -- add a valid RewriteRule (see [Apache documentation](http://httpd.apache.org/docs/2.2/mod/mod_rewrite.html#rewriterule)). In the example above, this would be...

        RewriteRule ^/projects/devpreview/releasenotes(.*)$ http://website-archive.mozilla.org/www.mozilla.org/devpreview_releasenotes/projects/devpreview/releasenotes$1 [L,R=301]

3. Commit your changes and submit a pull request.

### 10. Verify the redirect

Once the new RewriteRule is in production, requests to the original URL should redirect to the archive URL. Wait until this is true.

### 11. Delete the original content from the www.mozilla.org SVN tree 

The final step is to remove the old content from the www.mozilla.org SVN tree. If you are not comfortable with this step, you can open a new bug for this change.

1. Checkout the relevant SVN tree ([.org](http://svn.mozilla.org/projects/mozilla.org/trunk/), [.com](http://svn.mozilla.org/projects/mozilla.com/trunk/)).  

2. Remove the folder you've archived.

3. Commit your changes.

