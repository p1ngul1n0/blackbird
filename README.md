<img alt="blackbird-logo" align="left" width="300" height="300" src="https://raw.githubusercontent.com/p1ngul1n0/badges/main/badges/22.png">
<h1>Blackbird</h1>

### An OSINT tool to search fast for accounts by username across 581 sites.
> The Lockheed SR-71 "Blackbird" is a long-range, high-altitude, Mach 3+ strategic reconnaissance aircraft developed and manufactured by the American aerospace company Lockheed Corporation.

</br>

<img alt="blackbird-cli" align="center" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_printscreen.png">
<img alt="blackbird-web" align="center" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_web.png">

## Sponsors
This project is proudly sponsored by:

[<img alt="Cyber Hunter Lab Logo" align="center" width="20%" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/logo_chl.jpg" />](https://site.cyberhunteracademy.com/)

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

## NEWS❗
Blackbird is now available for use online https://blackbird-osint.herokuapp.com/

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
Access [http://127.0.0.1:9797](http://127.0.0.1:9797/) on the browser

#### Read results file
```python
python blackbird.py -f username.json
```
#### List supported sites
```python
python blackbird.py --list-sites
```
#### Use proxy
```python
python blackbird.py -u crash --proxy http://127.0.0.1:8080
```
#### Show all results
By default only found accounts will be shown, however you can use the argument below to see all of them.
```python
python blackbird.py -u crash --show-all
```
#### Export results to CSV file
```python
python blackbird.py -u crash --csv
```

## Docker
Blackbird can also be used with Docker.
#### Pull Image
```
docker pull p1ngul1n0/blackbird
```
#### Run Webserver
```
docker run -p 9797:9797 p1ngul1n0/blackbird "--web"
```

## Supported Social Networks <a name="social-networks"></a> ![](https://img.shields.io/badge/574--red)
#### Most of the sites on this list were obtained through the incredible <a href="https://github.com/WebBreacher/WhatsMyName">@whatsmynameproj</a> project, don't forget to visit and follow <a href="https://twitter.com/whatsmynameproj">them</a> . 🤟
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
21. AskFM
22. Vimeo
23. Pastebin
24. WordPress Profile
25. WordPress Site
26. AllMyLinks
27. Buzzfeed
28. JsFiddle
29. Sourceforge
30. Kickstarter
31. Smule
32. Blogspot
33. Tradingview
34. Internet Archive
35. Alura
36. Behance
37. MySpace
38. Disqus
39. Slideshare
40. Rumble
41. Ebay
42. RedBubble
43. Kik
44. Roblox
45. Armor Games
46. Fortnite Tracker
47. Duolingo
48. Chess
49. Shopify
50. Untappd
51. Last FM
52. Cash APP
53. Imgur
54. Trello
55. Minecraft
56. Patreon
57. DockerHub
58. Kongregate
59. Vine
60. Gamespot
61. Shutterstock
62. Chaturbate
63. ProtonMail
64. TripAdvisor
65. RapidAPI
66. HackTheBox
67. Wikipedia
68. Buymeacoffe
69. Arduino
70. League of Legends Tracker
71. Lego Ideas
72. Fiverr
73. Redtube
74. Dribble
75. Packet Storm Security
76. Ello
77. Medium
78. Hackaday
79. Keybase
80. HackerOne
81. BugCrowd
82. OneCompiler
83. TryHackMe
84. Lyrics Training
85. Expo
86. RAWG
87. Coroflot
88. Cloudflare
89. Wattpad
90. Mixlr
91. ImageShack
92. Freelancer
93. Dev To
94. BitBucket
95. Ko Fi
96. Flickr
97. HackerEarth
98. Spotify
99. Snapchat Stories
100. Audio Jungle
101. Avid Community
102. Bandlab
103. Carrd
104. CastingCallClub
105. Coderwall
106. Codewars
107. F3
108. Gab
109. Issuu
110. Steemit
111. Venmo
112. MODDB
113. COLOURlovers
114. Scheme Color
115. Roblox Trade
116. Aetherhub
117. BugBounty
118. Huntr
119. Universocraft
120. Wireclub
121. AminoApps
122. Trakt
123. Giphy
124. Minecraft List
125. SEOClerks
126. Mix
127. Codecademy
128. Bandcamp
129. Poshmark
130. hackster
131. BodyBuilding
132. Mastodon
133. IFTTT
134. Anime Planet
135. Destructoid
136. Gitee
137. Teknik
138. BitChute
139. The Tatto Forum
140. NPM
141. PyPI
142. HackenProof
143. VKontakte
144. About me
145. Dissenter
146. Designspiration
147. Fark
148. mmorpg
149. Pikabu
150. Playstation Network
151. Warrior Forum
152. Pxilart
153. 2Dimensions
154. 3dnews
155. 7Cups
156. 9GAG
157. Academia.edu
158. Airbit
159. Airliners
160. Alik.cz
161. Apple Developer
162. Apple Discussions
163. Asciinema
164. Ask Fedora
165. Audiojungle
166. Autofrage
167. BLIP.fm
168. Bazar.cz
169. Bezuzyteczna
170. Bikemap
171. BioHacking
172. Bitwarden Forum
173. 101010 pl
174. 3DNews
175. 7cup
176. 21buttons
177. about me
178. Adult_Forum
179. ADVFN
180. aflam
181. akniga
182. Albicla
183. allesovercrypto
184. allmylinks
185. Alloannonces
186. AllTrails
187. Ameblo
188. AmericanThinker
189. Aminoapps
190. AnimePlanet
191. aNobii
192. anonup
193. Apex Legends
194. Appian
195. Archive Of Our Own Account
196. ArmorGames
197. ArtBreeder
198. Artists & Clients
199. asciinema
200. ask fm
201. au ru
202. authorSTREAM
203. Ayfal
204. bblog_ru
205. BDSMLR
206. bdsmsingles
207. Bentbox
208. BiggerPockets
209. Bimpos
210. Bitbucket
211. Bitchute
212. bitcoin forum
213. BLIP fm
214. Blogger
215. blogi pl
216. Blogmarks
217. BodyBuilding com
218. Bookcrossing
219. Booth
220. Brickset
221. Bugcrowd
222. buymeacoffee
223. BuzzFeed
224. Buzznet
225. Carbonmade
226. Career habr
227. CaringBridge
228. carrd co
229. cash app
230. CD-Action
231. cda pl
232. championat
233. Chaos social
234. cHEEZburger
235. Chamsko
236. Chess com
237. Chomikuj pl
238. Chyoa
239. clusterdafrica
240. cnet
241. codeforces
242. codementor
243. contactos sex
244. coroflot
245. cracked_io
246. Cracked
247. crevado
248. crowdin
249. Cults3D
250. Cytoid
251. Dailymotion
252. darudar
253. dateinasia
254. datezone
255. Dating ru
256. Demotywatory
257. Designspriation
258. DeviantArt
259. dfgames
260. dev to
261. devRant
262. Diablo
263. diigo
264. Digitalspy
265. Discogs
266. Discourse
267. discuss elastic co
268. Dojoverse
269. Dribbble
270. Droners
271. easyen
272. eBay
273. Elftown
274. Ello co
275. Engadget
276. EPORNER
277. Etsy
278. EU_Voice
279. ExtraLunchMoney
280. Eyeem
281. Fabswingers
282. Facenama
283. Faktopedia
284. FanCentro
285. Fandom
286. fanpop
287. fansly
288. FatSecret
289. fcv
290. fedi lewactwo pl
291. Filmweb
292. Flipboard
293. Fodors Forum
294. forumprawne org
295. fotka
296. Foursquare
297. freelancer
298. freesound
299. FriendFinder
300. FriendFinder-X
301. Friendweb
302. FurAffinity
303. Furiffic
304. game_debate
305. Garmin connect
306. Geocaching
307. getmonero
308. Gettr
309. Gigapan
310. Girlfriendsmeet
311. gitea
312. GitHub
313. GitLab
314. gitee
315. gloria tv
316. gnome_extensions
317. gpodder net
318. grandprof
319. Gravatar
320. gumroad
321. Hacker News
322. Hackernoon
323. hackerearth
324. hamaha
325. Heylink
326. hiberworld
327. HomeDesign3D
328. Houzz
329. HubPages
330. Hubski
331. hugging_face
332. Iconfinder
333. icq-chat
334. ifunny
335. igromania
336. ilovegrowingmarijuana
337. imagefap
338. iMGSRC RU
339. imgur
340. Independent academia
341. InkBunny
342. InsaneJournal
343. instructables
344. Internet Archive Account
345. Internet Archive User Search
346. interpals
347. ipolska pl
348. issuu
349. JBZD
350. jeja pl
351. Jeuxvideo
352. Joe Monster
353. JSFiddle
354. Justforfans
355. kaggle
356. karab in
357. kik
358. Ko-Fi
359. Kotburger
360. kwejk pl
361. LibraryThing
362. lichess
363. LINE
364. linux org ru
365. Livejournal
366. lobste rs
367. lowcygier pl
368. MAGABOOK
369. MAGA-CHAT
370. Magix
371. MapMyTracks
372. Maroc_nl
373. Marshmallow
374. Martech
375. Massage Anywhere
376. mastodon
377. MCUUID (Minecraft)
378. medyczka pl
379. meet me
380. megamodels pl
381. memrise
382. Microsoft Technet Community
383. Minds
384. Mistrzowie
385. Mixi
386. Mmorpg
387. Mod DB
388. Moneysavingexpert
389. Motokiller
390. moxfield
391. Muck Rack
392. MyAnimeList
393. MyBuilder com
394. MyFitnessPal
395. my_instants
396. MyLot
397. mym fans
398. NameMC
399. naija_planet
400. nairaland
401. NaturalNews
402. Naver
403. netvibes
404. Newgrounds
405. newmeet
406. NotABug
407. oglaszamy24h pl
408. ok ru
409. okidoki
410. olx
411. Opencollective
412. OpenStreetMap
413. OPGG
414. Orbys
415. osu!
416. Our Freedom Book
417. ow ly
418. palnet
419. Parler
420. Parler archived profile
421. Parler archived posts
422. PatientsLikeMe
423. Patronite
424. PCGamer
425. PCPartPicker
426. Pewex
427. Photoblog
428. PhotoBucket
429. Picsart
430. Piekielni
431. pikabu
432. PinkBike
433. Plurk
434. Pokec
435. pokemonshowdown
436. Pokerstrategy
437. Polchat pl
438. policja2009
439. Poll Everywhere
440. pol social
441. polygon
442. popl
443. Pornhub Porn Stars
444. Pornhub Users
445. postcrossing
446. Producthunt
447. promodj
448. prv pl
449. public
450. QUEER
451. quitter pl
452. Quora
453. ReblogMe
454. redbubble
455. Researchgate
456. rigcz club
457. risk ru
458. rsi
459. Ruby Dating
460. RumbleChannel
461. RumbleUser
462. Salon24
463. SaraCarterShow
464. ScoutWiki
465. scratch
466. Seneporno
467. sentimente
468. setlist fm
469. SFD
470. Shanii Writes
471. Shesfreaky
472. shopify
473. shutterstock
474. skeb
475. Skypli
476. Skyrock
477. slant
478. slideshare
479. slides
480. SmashRun
481. smelsy
482. SmugMug
483. smule
484. soc citizen4 eu
485. SoliKick
486. SoundCloud
487. Soup
488. SpankPay
489. Speaker Deck
490. SpiceWorks
491. sporcle
492. steemit
493. StoryCorps
494. Stripchat
495. sukebei nyaa si
496. Suzuri
497. Swalifnet
498. szmer info
499. tabletoptournament
500. Tagged
501. TamTam
502. Tanuki pl
503. Taringa
504. taskrabbit
505. Teamtreehouse
506. Tellonym
507. TF2 Backpack Examiner
508. tfl net pl
509. thegatewaypundit
510. theguardian
511. themeforest
512. Thetattooforum
513. TotalWar
514. TrackmaniaLadder
515. tradingview
516. trakt
517. tripadvisor
518. tumblr
519. Tunefind
520. Twitcasting
521. Twitch
522. Twitter archived profile
523. Twitter archived tweets
524. twpro
525. Udemy
526. uid
527. Ultras Diary
528. ulub pl
529. unsplash
530. untappd
531. USA Life
532. Vero
533. vibilagare
534. viddler
535. VIP-blog
536. Virustotal
537. Vivino
538. vizjer pl
539. VK
540. Voice123
541. Voices com
542. vsco
543. Wanelo
544. warriorforum
545. watchmemore com
546. wattpad
547. Weasyl
548. wego
549. weheartit
550. weibo
551. Wikidot
552. Wimkin-PublicProfile
553. wishlistr
554. Wolni Słowianie
555. wordnik
556. WordPress
557. WordPress Support
558. Wowhead
559. Wykop
560. Xanga
561. xHamster
562. Xing
563. XVIDEOS-models
564. XVIDEOS-profiles
565. Yahoo! JAPAN Auction
566. Yazawaj
567. Yelp
568. zatrybi pl
569. Zbiornik
570. zhihu
571. Zillow
572. zmarsa com
573. Zomato
574. zoomitir
575. Zepeto
576. YouPic
577. VIEWBUG
578. Art Limited
579. 35photo.pro
580. Purple Port
581. Pixieset

</details>

## Export Report
The results can be exported as a PDF Report.
<p float="left" align="center">
  <img alt="blackbird-pdf-cover" width="300" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_report_pdf_cover.png">
  <img alt="blackbird-pdf-cover" width="300" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_report_pdf_results.png">
</p>

## Metadata Extraction
When possible Blackbird will extract the user's metadata, bringing data such as name, bio, location and profile picture.

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

## FrontEnd
Blackbird FrontEnd is made with React JS, you can see the source code [here](https://github.com/p1ngul1n0/blackbird-react).

## Contributors 🏅
<a href="https://github.com/p1ngul1n0/blackbird/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=p1ngul1n0/blackbird" />
</a>

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
- <a href="https://github.com/LsvanDarko">@LsvanDarko</a> - Added requests package to requirements.txt.
- <a href="https://github.com/wymiotkloaki">@wymiotkloaki</a> - Added basic .gitignore file and 21 sites.
- <a href="https://github.com/dwaltsch">@dwaltsch</a> - Added Dockerfile.
- <a href="https://github.com/yutodadil">@yutodadil</a> - Added Zepeto and increased timeout to 10 seconds.
- <a href="https://github.com/Pitastic">@pitastic</a> - Fixed <a href="https://github.com/p1ngul1n0/blackbird/issues/42">Access to 127.0.0.1 was denied #42 </a> issue.
- <a href="https://github.com/qqux">@qqux</a> - Added 6 sites (YouPic, VIEWBUG, Art Limited, 35photo.pro, Purple Port, Pixieset).

## Planned features

- [X] Implement Flask Web Server to optimize UX
- [X] Export results in PDF
- [X] Implement metadata extraction
- [X] Publish a docker image
- [ ] Add unit test (Change ID to Appname, add "invalid-user" and "valid-user" params in JSON.)
- [ ] Export results in CSV
- [X] Deploy on Cloud


## Contact
Feel free to contact me on <a href="https://twitter.com/p1ngul1n0">Twitter</a>
