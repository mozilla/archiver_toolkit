import os
import argparse
import fnmatch
from datetime import datetime
from bs4 import BeautifulSoup
from bs4 import Comment


def locate(pattern, root):
    '''recursive directory pattern search'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)


def readable_dir(prospective_dir):
    '''verify the argument is a valid dir'''
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError(
            "{0} is not a valid path".format(prospective_dir)
        )
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError(
            "{0} is not a readable dir".format(prospective_dir)
        )


# parse arguments
parser = argparse.ArgumentParser(description='Process a directory of content.')
parser.add_argument('directory',
                    help='directory to process',
                    type=readable_dir,
                    action='store')
args = parser.parse_args()


# define strings to replace, strings to insert
css = '''
    body { padding-top: 25px; }
    #archived { margin: 0; padding: 5px; position: absolute; top: 0;
    left: 0; height: 25px; width: 100%; z-index: 1000;
    text-align: center;
    font: bold 1.143em/1 Arial, Calibri, Helvetica, "Helvetica Neue";
    color: #f5f3ed; background-color: #4d5151; }
    #archived a { color: #fff; }
    #archived a:hover { color: #fff; text-decoration: underline; }
'''

text = 'You are viewing information archived from Mozilla.org on %s.' % (
    datetime.utcnow().strftime("%Y-%m-%d")
    )


# process every file
for filename in locate("*.html", args.directory):

    with open(filename, "r") as f:
        soup = BeautifulSoup(f)

    if len(soup.select('#archived')) == 0:
        print 'Processing %s' % (filename)

        # get rid of search form
        for s in soup.select('#quick-search'):
            s.replace_with(Comment('search removed'))

        # add styles for notification block
        style = soup.new_tag('style', type='text/css')
        style.append(css)
        soup.head.append(style)

        # add notification block
        div = soup.new_tag('div', id='archived')
        div.append(text)
        soup.body.insert(0, div)

        with open(filename, "w") as f:
            f.write(str(soup))
