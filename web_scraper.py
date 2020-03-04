import time
import sys
import os
import argparse
import concurrent.futures


#This will create a list of search terms:
# common_names = tree.xpath('//li/a[1][starts-with(@href, "/wiki/")]/text()')
# selects text from the first a tag nested within an li with an href values that starts with /wiki/


# Flora of California according to wikipedia
objects = ['Coast redwood',
'Giant sequoia',
'Bishop pine',
'Coulter pine',
'Gray pine',
'Knobcone pine',
'Ponderosa pine',
'Lodgepole pine',
'Monterey pine',
'Limber pine']
# 'Jeffrey pine',
# 'Parry pinyon',
# 'Shore pine',
# 'Sugar pine',
# 'Torrey pine',
# 'Western white pine',
# 'Single-leaf pinyon pine',
# 'Great Basin bristlecone pine',
# 'Foxtail pine',
# 'Monterey cypress',
# 'Santa Lucia fir',
# 'Douglas-fir',
# 'Bigcone Douglas-fir',
# 'California nutmeg',
# 'Incense cedar',
# 'Port Orford cedar-Lawson cypress',
# 'White fir',
# 'Mountain hemlock',
# 'Red fir',
# 'Pacific yew',
# 'Valley oak',
# 'Leather oak',
# 'Blue oak',
# 'California black oak',
# 'Canyon live oak',
# 'Interior live oak',
# 'Island oak',
# 'Engelmann oak',
# 'Coast live oak',
# 'California sycamore',
# 'White alder',
# 'Quaking aspen',
# 'Fremont cottonwood',
# 'Black cottonwood',
# 'Arroyo willow',
# 'Tanoak',
# 'California bay laurel',
# 'Madrone',
# 'Toyon',
# 'Bigleaf maple',
# 'Western blue elderberry',
# 'California Buckeye',
# 'Western redbud',
# 'California black walnut',
# 'California hazelnut',
# 'Chamise',
# 'Service-berry',
# 'Manzanita',
# 'California sagebrush',
# 'Coyote brush',
# 'Calliandra',
# 'California lilacs',
# 'Desert willow',
# 'Flannelbush',
# 'Creosote bush',
# 'Lupines',
# 'Snowberry',
# 'Huckleberry',
# 'Coffeeberry',
# 'Lemonade berry',
# 'Sugarbush',
# 'Gooseberries and currants',
# 'Sages',
# 'California fan palm',
# 'Joshua tree',
# 'California juniper',
# 'Blue palo verde',
# 'Yellow foothill palo verde',
# 'Single-leaf pinyon',
# 'Fremont cottonwood',
# 'Ocotillo',
# 'Creosote bush',
# 'Indian mallow',
# 'Brittlebush',
# 'Desert agave',
# 'California barrel cactus',
# 'Banana yucca',
# 'Mojave yucca',
# 'Rush milkweed',
# 'Purple desert sand-verbena',
# 'Sacred datura',
# 'California poppy',
# 'Douglas iris',
# 'Monkeyflower',
# 'Columbine',
# 'Coyote mint',
# 'Buckwheats',
# 'Western wild ginger',
# 'Pacific bleeding-heart',
# 'Island coral bells',
# 'Canyon coral bells',
# 'Heucherella',
# 'Threeleaf foamflower',
# 'Redwood sorrel',
# 'Polypody ferns',
# 'Native sword ferns',
# 'Giant chain fern',
# 'Goldback ferns',
# 'Wood ferns',
# 'Maidenhair ferns',
# "Ithuriel's spear",
# 'Meadow onion',
# 'Goldenstars',
# 'Brodiaeas',
# 'Blue dicks-ookow',
# 'Mariposa lilies',
# 'Baby blue eyes',
# 'Blazing star',
# 'California poppy',
# 'Chinese houses',
# 'Elegant clarkia',
# 'Farewell-to-spring',
# 'Meadowfoam',
# "Miner's lettuce",
# 'Tarweed',
# 'Wind poppy',
# "Dutchman's pipe vine",
# 'Morning glory',
# 'Chaparral clematis',
# "Western virgin's bower",
# 'Calabazilla',
# 'Wild cucumber-manroot',
# 'Cucamonga manroot-bigroot',
# 'California wild grape',
# 'Desert wild grape',
# 'Purple three-awn',
# 'Blue grama',
# 'California fescue',
# 'Idaho fescue',
# 'Red fescue',
# 'Junegrass',
# 'Giant wildrye',
# 'California melic',
# 'Deer grass',
# 'Purple needlegrass',
# 'Indian ricegrass',
# 'Pine bluegrass',
# 'Sedges',
# 'Rushes',
# 'Western blue-eyed grass',
# 'Chalk lettuce',
# 'Coast dudleya',
# 'Canyon live-forever',
# 'Fingertips',
# "Giant chalk dudleya",
# 'Lanceleaf liveforever',
# 'Broadleaf stonecrop',
# 'Coast sedum',
# 'Feather River stonecrop',
# 'Red Mountain stonecrop',
# 'Roseflower stonecrop',
# 'Sierra stonecrop']


# Taking command line arguments from users
parser = argparse.ArgumentParser()
# parser.add_argument('-k', '--keywords', help='delimited list input', type=str, required=True)
parser.add_argument('-l', '--limit', help='delimited list input', type=str, required=False)
parser.add_argument('-c', '--color', help='filter on color', type=str, required=False, choices=['red', 'orange', 'yellow', 'green',
	'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown'])
parser.add_argument('-s', '--size', help='filter on size', type=str, required=False, choices=['any', 'large', 'medium', 'icon'])

args = parser.parse_args()
# search_keyword = [str(item) for item in args.keywords.split(',')]
#setting limit on number of images to be downloaded
if args.limit:
    limit = int(args.limit)
    if int(args.limit) >= 100:
        limit = 100
else:
    limit = 100

# keyword_param = args.keywords.replace(' ', '+')
color_param = (',ic:specific,isc:' + args.color) if args.color else ''
size_param = (',isz:'+args.size[0]) if args.size else ''


# Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3, 0)
    cur_version = sys.version_info
    if cur_version >= version:  # If the Current Version of Python is 3.0 or above
        import urllib.request  # urllib library for Extracting web pages
        try:
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:  # If the Current Version of Python is 2.x
        import urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers=headers)
            try:
                response = urllib2.urlopen(req)
            except URLError: # Handling SSL certificate failed
                context = ssl._create_unverified_context()
                response = urlopen(req,context=context)
            page = response.read()
            return page
        except:
            return "Page Not found"


# Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line + 1)
        end_content = s.find(',"ow"', start_content + 1)
        content_raw = str(s[start_content + 6:end_content - 1])
        return content_raw, end_content


# Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            # only want jpg images...
            
            items.append(item)  # Append all the links in the list named 'Links'
            time.sleep(0.1)  # Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items

def save_images(obj):
	keyword_param = obj.replace(' ', '+')

	url = ('https://www.google.com/search?as_st=y&tbm=isch&hl=en&as_q="'+keyword_param+
	      '"&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=itp:photo'+size_param+color_param+',ift:jpg'
	      )

	raw_html = (download_page(url))
	time.sleep(0.1)
	items = _images_get_all_items(raw_html)
	print ("Total Image Links = " + str(len(items)))

	dir_name = keyword_param.replace('+', '_')
	os.makedirs(dir_name)

	## To save imges to the same directory
	# IN this saving process we are just skipping the URL if there is any error
	k = 0
	e = 0
	while (k < limit+e):    # I want limit num of images no matter what!!
	    try:
	        req = Request(items[k], headers={
	            "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
	        response = urlopen(req, None, 15)
	        image_name = str(items[k][(items[k].rfind('/'))+1:])
	        if '?' in image_name:
	            image_name = image_name[:image_name.find('?')]
	        if ".jpg" in image_name or ".png" in image_name or ".jpeg" in image_name or ".svg" in image_name:
	            output_file = open(dir_name + "/" + str(k + 1) + ". " + image_name, 'wb')
	        else:
	            output_file = open(dir_name + "/" + str(k + 1) + ". " + image_name + ".jpg", 'wb')
	            image_name = image_name + ".jpg"

	        data = response.read()
	        output_file.write(data)
	        response.close()

	        print("completed ====> " + str(k + 1) + ". " + image_name)
	        k += 1

	    except IOError:  # If there is any IOError

	        errorCount += 1
	        e += 1
	        print("IOError on image " + str(k + 1))
	        k += 1

	    except HTTPError as e:  # If there is any HTTPError

	        errorCount += 1
	        e += 1
	        print("HTTPError" + str(k))
	        k += 1
	    except URLError as e:

	        errorCount += 1
	        e += 1
	        print("URLError " + str(k))
	        k += 1



############## Main Program ############
t0 = time.time()  # start the timer

version = (3,0)
cur_version = sys.version_info
if cur_version >= version:  # If the Current Version of Python is 3.0 or above
    # urllib library for Extracting web pages
    from urllib.request import Request, urlopen
    from urllib.request import URLError, HTTPError

else:  # If the Current Version of Python is 2.x
    # urllib library for Extracting web pages
    from urllib2 import Request, urlopen
    from urllib2 import URLError, HTTPError

# Download Image Links
errorCount = 0



with concurrent.futures.ProcessPoolExecutor() as executor:
# for obj in objects:
	executor.map(save_images, objects)



print("\n")
print("Everything downloaded!")

t1 = time.time()  # stop the timer
total_time = t1 - t0  # Calculating the total time required to crawl, find and download all the links of 60,000 images
print("Total time taken: " + str(total_time) + " Seconds")
print("Total Errors: "+ str(errorCount) + "\n")