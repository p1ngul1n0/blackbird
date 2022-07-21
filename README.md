<img alt="blackbird-logo" align="left" width="300" height="300" src="https://github.com/p1ngul1n0/badges/blob/main/badges/20.png">
<h1>Blackbird</h1>

### An OSINT tool to search fast for accounts by username across 144 sites.
> The Lockheed SR-71 "Blackbird" is a long-range, high-altitude, Mach 3+ strategic reconnaissance aircraft developed and manufactured by the American aerospace company Lockheed Corporation.

</br></br></br>

<img alt="blackbird-cli" align="center" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_printscreen.png">
<img alt="blackbird-web" align="center" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_web.png">


## Disclaimer
```
This or previous program is for Educational purpose ONLY. Do not use it without permission. 
The usual disclaimer applies, especially the fact that me (P1ngul1n0) is not liable for any 
damages caused by direct or indirect use of the information or functionality provided by these 
programs. The author or any Internet provider bears NO responsibility for content or misuse 
of these programs or any derivatives thereof. By using these programs you accept the fact 
that any damage (dataloss, system crash, system compromise, etc.) caused by the use of these 
programs is not P1ngul1n0's responsibility.
```




## Setup

#### Clone the repository
```shell
git clone https://github.com/p1ngul1n0/blackbird
cd blackbird
```

#### Install requirements
```shell
pip install -r requirements.txt
```

## Usage

#### Search by username
```python
python blackbird.py -u username
```
#### Run WebServer
```python
python blackbird.py --web
```
Access [http://127.0.0.1:5000](http://127.0.0.1:5000/) on the browser

#### Read results file
```python
python blackbird.py -f username.json
```
#### List supported sites
```python
python blackbird.py --list-sites
```

## Supported Social Networks <a name="social-networks"></a> ![](https://img.shields.io/badge/144--red)
<details>
  <summary></summary>
  
1. Facebook
2. YouTube
3. Twitter
4. Telegram
5. TikTok
6. Tinder
7. Instagram
8. Pinterest
9. Snapchat
10. Reddit
11. Soundcloud
12. Github
13. Steam
14. Linktree
15. Xbox Gamertag
16. Twitter Archived
17. Xvideos
18. PornHub
19. Xhamster
20. Periscope
21. Ask FM
22. Vimeo
23. Twitch
24. Pastebin
25. WordPress Profile
26. WordPress Site
27. AllMyLinks
28. Buzzfeed
29. JsFiddle
30. Sourceforge
31. Kickstarter
32. Smule
33. Blogspot
34. Tradingview
35. Internet Archive
36. Alura
37. Behance
38. MySpace
39. Disqus
40. Slideshare
41. Rumble
42. Ebay
43. RedBubble
44. Kik
45. Roblox
46. Armor Games
47. Fortnite Tracker
48. Duolingo
49. Chess
50. Shopify
51. Untappd
52. Last FM
53. Cash APP
54. Imgur
55. Trello
56. Minecraft
57. Patreon
58. DockerHub
59. Kongregate
60. Vine
61. Gamespot
62. Shutterstock
63. Chaturbate
64. ProtonMail
65. TripAdvisor
66. RapidAPI
67. HackTheBox
68. Wikipedia
69. Buymeacoffe
70. Arduino
71. League of Legends Tracker
72. Lego Ideas
73. Fiverr
74. Redtube
75. Dribble
76. Packet Storm Security
77. Ello
78. Medium
79. Hackaday
80. Keybase
81. HackerOne
82. BugCrowd
83. OneCompiler
84. TryHackMe
85. Lyrics Training
86. Expo
87. RAWG
88. Coroflot
89. Cloudflare
90. Wattpad
91. Mixlr
92. ImageShack
93. Freelancer
94. Dev To
95. BitBucket
96. Ko Fi
97. Flickr
98. HackerEarth
99. Spotify
100. Snapchat Stories
101. Audio Jungle
102. Avid Community
103. Bandlab
104. Carrd
105. CastingCallClub
106. Coderwall
107. Codewars
108. F3
109. Gab
110. Issuu
111. Steemit
112. Venmo
113. MODDB
114. COLOURlovers
115. Scheme Color
116. Roblox Trade
117. Aetherhub
118. BugBounty
119. Huntr
120. Universocraft
121. Wireclub
122. AminoApps
123. Trakt
124. Giphy
125. Minecraft List
126. SEOClerks
127. Mix
128. Codecademy
129. Bandcamp
130. Poshmark
131. hackster
132. BodyBuilding
133. Mastodon
134. IFTTT
135. Anime Planet
136. Destructoid
137. Gitee
138. Teknik
139. BitChute
140. The Tatto Forum
141. NPM
142. PyPI
143. HackenProof
144. VKontakte
</details>

## Export Report
The results can be exported as a PDF Report.
<p float="left" align="center">
  <img alt="blackbird-pdf-cover" width="300" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_report_pdf_cover.png">
  <img alt="blackbird-pdf-cover" width="300" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_report_pdf_results.png">
</p>

## Metadata Extraction
When possible Blackbird will extract the user's metadata, bringing data such as name, bio, location and profile picture.

<img alt="blackbird-metadata" align="center" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_metadata.png">

## Random UserAgent
Blackbird uses a random UserAgent from a <a href="https://gist.github.com/pzb/b4b6f57144aea7827ae4">list of 1000 UserAgents</a> in each request to prevent blocking.

## Supersonic speed :rocket:
Blackbird sends async HTTP requests, allowing a lot more speed when discovering user accounts.

## JSON Template
<details>
  <summary></summary>
Blackbird uses JSON as a template to store and read data.

The <a href="https://github.com/p1ngul1n0/blackbird/blob/main/data.json">data.json</a> file store all sites that blackbird verify.


#### Params
- app - Site name
- url
- valid - Python expression that returns True when user exists
- id - Unique numeric  ID
- method - HTTP method
- json - JSON body POST (needs to be escaped, use this :point_right: https://codebeautify.org/json-escape-unescape)
- {username} - Username place (URL or Body)
- response.status - HTTP response status
- responseContent - Raw response body
- soup - Beautifulsoup parsed response body
- jsonData - JSON response body
- metadada - a list of objects to be scraped

#### Examples
GET
```JSON
    {
      "app": "ExampleAPP1",
      "url": "https://www.example.com/{username}",
      "valid": "response.status == 200",
      "id": 1,
      "method": "GET"
    }
```
POST JSON
```JSON
    {
      "app": "ExampleAPP2",
      "url": "https://www.example.com/user",
      "valid": "jsonData['message']['found'] == True",
      "json": "{{\"type\": \"username\",\"input\": \"{username}\"}}",
      "id": 2,
      "method": "POST"
    }
```
GET with Metadata extraction
```JSON
    {
      "app": "Twitter",
      "id": 3,
      "method": "GET",
      "url": "https://nitter.net/{username}",
      "valid": "response.status == 200",
      "metadata": [
        {
          "type": "generic-data",
          "key": "Name",
          "value": "soup.find('a', class_='profile-card-fullname')['title']"
        },
        {
          "type": "generic-data",
          "key": "Bio",
          "value": "soup.find('div',class_='profile-bio').string"
        },
        {
          "type": "generic-data",
          "key": "Site",
          "value": "soup.find('div',class_='profile-website').text.strip('\\t\\r\\n')"
        },
        {
          "type": "generic-data",
          "key": "Member since",
          "value": "soup.find('div',class_='profile-joindate').find('span')['title']"
        },
        {
          "type": "image",
          "key": "picture",
          "value": "'https://nitter.net'+soup.find('a', class_='profile-card-avatar')['href']"
        },
        {
          "type": "location",
          "key": "location",
          "value": "soup.select_one('.profile-location:nth-of-type(2)').text.strip('\\t\\r\\n')"
        }
      ]
    }
```
If you have any suggestion of a site to be included in the search, make a pull request following the template.
</details>

## Contributors 🏅
I'm grateful to all contributors who improved and bugfixed the project.

- <a href="https://github.com/RelatedTitle">@RelatedTitle</a> - Fixed the Youtube user search URL.
- <a href="https://github.com/prisar">@prisar</a> - Fixed the OS check for AsyncIO policy.
- <a href="https://github.com/itmaru">@itmaru</a> - Fixed 'across' typo.
- <a href="https://github.com/Bryan-Herrera-DEV">@Bryan-Herrera-DEV</a> - Added Universocraft site.
- <a href="https://github.com/devXprite">@devXprite</a> - Added NPM and PyPI sites.
- <a href="https://github.com/ChrisCarini">@ChrisCarini</a> - Fixed 'supported' typo.
- <a href="https://github.com/Pandede">@Pandede</a> - Fixed <a href="https://github.com/p1ngul1n0/blackbird/issues/24">No such file or directory: 'python' #24 </a> issue, reformatted with autopep8, implemented `enumerate` and code splitting for functions.
- <a href="https://github.com/tr33n">@tr33n</a> - Implemented random UserAgent for each request.
- <a href="https://github.com/Sebsebzen">@Sebsebzen</a> - Added VKontakte (with metadata).

## Planned features

- [X] Implement Flask Web Server to optimize UX
- [X] Export results in PDF
- [ ] Export results in CSV
- [X] Implement metadata extraction
- [ ] Deploy on Cloud

## Contact
Feel free to contact me on <a href="https://twitter.com/p1ngul1n0">Twitter</a>
