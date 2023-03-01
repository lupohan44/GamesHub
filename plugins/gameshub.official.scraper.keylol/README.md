# Keylol Scraper (gameshub.official.scraper.keylol)

## Description
This is plugin to scrap free games information from [Keylol](https://keylol.com/t572814-1-1)  
currently only support steam free games  
cookies is not required but strongly recommended, plugin will rate for the post to say "thank you" to the post author.
![rate.png](../../static_files/rate.png)
## [Requirements](requirements.txt)

## FAQ
### 1. How to get cookies?
1. Login to [Keylol](https://keylol.com/)
2. Open developer tools (F12)
3. Go to Network tab
4. Refresh the page
5. Find a request to `https://keylol.com/`
6. Copy the value of `Cookie` header in `Headers` tab into `cookies.txt`
![cookies.png](../../static_files/cookies.png)

## Changelog
v1.0.4
- cookies is not required anymore

v1.0.3
- Redeem using appid should add 'a/' prefix, using subid should add 's/' prefix

v1.0.2
- Scraper will now return free sub_id in information and in extra_information, return app_id in url

v1.0.1
- Fix scraper get wrong information when steam url is like https://store.steampowered.com/sub/xxxx

v1.0.0
- Initial release
