## Synopsis
This is a simple bit of code that unobscures the numbers on a trading card game web portal into a json format. The numbers are obscured using randomness, some images, and a handful of red herrings. 

## Requirements
You will need **node** (I've got 6.2.1. it should work with older versions) and **Python2.7**. The node dependencies are described in package.json, and can be easily installed by running **npm install**.

In order for the python part to work, you're going to need to **pip install** the following packages:

beautifulsoup4 (might have to **easy_install** this one depending on your setup)

requests

urllib

PIL - Python Image Library

ImageChops

## Example Output
In order to run simply **"npm start"** (or *node server.js*) inside the base directory. This will fire up an express web server that you can access at http://localhost:9090. Pricing json is returned at the /json endpoint. For example, Opening up **http://localhost:9090/json/shu yun, the silent tempest** will return the following: 

{"Shu Yun, the Silent Tempest": {"Fate Reforged (Foil)": {"NM/M": "1.99"}, "Fate Reforged": {"NM/M": "0.49"}}, "Shu Yun, the Silent Tempest (Fate Reforged)": {"Non-English Singles: Korean": {"NM/M": "0.99"}}, "Shu Yun, the Silent Tempest (Fate Reforged Prerelease)": {"Promotional Cards: Prerelease & Launch (Foil)": {"SP": "0.79", "NM/M": "0.99"}}}

You can test the whole thing in your browser. 

Note -- if you want to simply run the python script that does the heavy lifting (you'll still need node for some quick tricks) you can do so by running:

**python cut_img.py card-name-here" 

## Motivation
I created this *because* it was challenging. I'm posting it here only for educational purposes. I found it very interesting how these prices were obscured, and I wanted to see how difficult it would be to reverse that process. This is probably not fast enough for a production app anyway, but it goes without saying -- use it at your own risk. I assume no liability for what you do from here on out.

## Contributors
This really is intended as a proof-of-concept. It runs fairly quickly if the cards are not in many sets, but takes longer for cards with multiple sets (eg - fireball). The run time can definitely be improved, and if you are interested in contributing, go for it. Do a pull, make a fork, suggest edits, whatever you'd like. Feel free to message me directly. 

## Legal
The intended use of any code found in this repository is for teaching, criticism, scholarship and research. You should not run this code. I assume no responsibility for any derivative works, or unintended uses. Thanks. I hope you enjoy it.

### How Are the Numbers Obscured Anyway?
Each time you load a page, an image containing the digits one to nine is generated. The order of the numbers is random.
Along with this image, css is generated that describes how to display each number. Both of these are *different each time*. All numbers on the page are replaced with an image styled by the appropriate css. Some of the css is not even used. The image seems to expire. 

Each number that you see on the page is the *same image* but with different styles applied - This causes only the relevant number to be shown. I'm not sure if this is an out of the box solution, or some kind of custom job. In order to reverse this process...well, check out the code.


#### the moving parts:
server.js -- an express web server to serve up the content from :

cut_img.py -- a python script that grabs all of the relevant stuff and analyzes it to produce the output

css2json.js -- a node script that converts the css to a parse-able json format
