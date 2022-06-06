<img alt="blackbird-logo" align="left" width="300" height="300" src="https://github.com/p1ngul1n0/badges/blob/main/badges/20.png">
<h1>Blackbird</h1>

### An OSINT tool to search fast for accounts by username across 101 sites.
> The Lockheed SR-71 "Blackbird" is a long-range, high-altitude, Mach 3+ strategic reconnaissance aircraft developed and manufactured by the American aerospace company Lockheed Corporation.

</br></br></br></br>


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
<img alt="blackbird-web" align="center" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_web.png">
<img alt="blackbird-cli" align="center" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_printscreen.png">



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
#### List supportted sites
```python
python blackbird.py --list-sites
```

## Supported Social Networks <a name="social-networks"></a> ![](https://img.shields.io/badge/101--red)
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
56. MCUUID Minecraft
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
83. DevPost
84. OneCompiler
85. TryHackMe
86. Lyrics Training
87. Expo
88. RAWG
89. Coroflot
90. Cloudflare
91. Wattpad
92. Mixlr
93. ImageShack
94. Freelancer
95. Dev To
96. BitBucket
97. Ko Fi
98. Flickr
99. HackerEarth
100. Spotify
101. Snapchat Stories
</details>

## Supersonic speed :rocket:
Blackbird sends async HTTP requests, allowing a lot more speed when discovering user accounts.

## JSON Template
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

If you have any suggestion of a site to be included in the search, make a pull request following the template.

## Contact
Feel free to contact me on <a href="https://twitter.com/p1ngul1n0">Twitter</a>
