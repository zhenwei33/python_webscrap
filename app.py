import os
from selenium import webdriver

op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")

driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options= op)

# driver.get("https://youtube.com")
# print(driver.page_source)

channelIds = [
    'UCSJ4gkVC6NrvII8umztf0Ow',
    'UCzMxEa-lDX2AfgotszScOFg',
    'UCsIg9WMfxjZZvwROleiVsQg',
    # 'UChs0pSaEoNLV4mevBFGaoKA'

    'UC1opHUrw8rvnsadT-iGp7Cg', #aqua
    'UC-hM6YJuNYVAmUWxeIr9FeA', # miko
    'UC1DCedRgGHBdm81E1llLhOQ', # pekora
    'UCvzGlP9oQwU--Y0r9id_jnA', # subaru
    'UCqm3BQLlJfvkTsX_hvm0UmA', # watame
    'UCCzUftO8KOVkV4wQG1vkUvg', # marine
    'UCMwGHR0BTZuLsmjY_NT5Pwg', #ninomae
    'UCD-miitqNY3nyukJ4Fnf4_A', #tsukino
]

remaining_channelIds = channelIds
baseUrl = 'https://www.youtube.com'

class Channel():
    def __init__(self, name, profileUrl, videos):
        self.name = name
        self.profileUrl = profileUrl
        self.videos = videos

    # def set_videos(self, videos):
    #     self.videos = videos
    def getName(self):
        return self.name

    def getVideos(self):
        return self.videos

class Video:
    def __init__(self, title, thumbnailUrl, url, view):
        self.title = title
        self.thumbnailUrl = thumbnailUrl
        self.url = url
        self.view = view

    def getTitle(self):
        return self.title

channel_list = []

def main():
    for channelId in channelIds:
        if (len(channel_list) < 5):
            driver.get('{}/channel/{}'.format(baseUrl, channelId))
            content = driver.page_source.encode('utf-8').strip()
            # Channel details
            name = driver.find_element_by_xpath('//*[@id="text-container"]/yt-formatted-string').text
            profileUrl = driver.find_element_by_xpath('//*[@id="avatar"]/img').get_attribute('src')
            video_list = []
            is_live = 0
            # Video details
            titles = driver.find_elements_by_xpath('//*[@id="video-title"]/yt-formatted-string')
            thumbnailUrls = driver.find_elements_by_xpath('//*[@id="thumbnail"]/yt-img-shadow/img')
            urls = driver.find_elements_by_xpath('//*[@id="thumbnail"]')
            views = driver.find_elements_by_xpath('//*[@id="metadata-line"]')
            
            # print(name)
            # print(profileUrl)
            # print(len(titles))
            for i in range(len(titles)):
                view = views[i].text
                if (view.split()[1] == 'watching'): # else 'waiting'
                    title = titles[i].text
                    thumbnailUrl = thumbnailUrls[i].get_attribute('src')
                    url = urls[i].get_attribute('href')
                    is_live = is_live + 1
                    
                    # print(title) # title
                    # print(thumbnailUrl) # thumbnailUrl
                    # print(url) # url
                    # print(view) # view

                    video = Video(title, thumbnailUrl, url, view)
                    video_list.append(video)
            
            if (is_live > 0):
                channel = Channel(name, profileUrl, video_list)
                channel_list.append(channel)
                # channel_live += 1
                print(channel.getName())
        else:
            break
    # print(channel_list[0].getName())
    # print(channel_list[0].getVideos()[0].getTitle())

# try: 
main()
driver.quit()
