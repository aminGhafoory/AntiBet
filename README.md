# AntiBet
![stop](https://i.ibb.co/5BCcYCt/stop.jpg)
## How To USe
1. visit [telegram](https://my.telegram.org/auth?to=apps) website and get a api-hash and api-key
2. Replace api_id and api_hash values with your own in `config.ini` file (without quotes).
3. replace your id (username) as robot admin in `config.ini` file
4. replcae your phone number in `config.ini` file
5. changing other setting is not necessery
6. run this command `$ chmod +x wrapper.sh`(in linux machine or WSL)
7. run this command and login to your  telegram account`$ ./wrapper.sh`
8. you can use this application just like this but if you want to dockerize it follow next steps
9. build an image with all of newly generated files using this command `docker build -t antibet:latest .`
10. now you can run your own containers;
11. use this command for running a container`docker run -d -p 8000:8000 antibet:latest`
12. this app will make an api for accessing gatherd link in `localhost:8000/links` 
13. after running the container send `!help` command to any private chat(saved messages for example) the robot will respond with all the available commands
14. have fun 🎈 


```
⭕️**help**
    🔰**__join :__**  `!join|link or id`
    example:
    `!join|https://t.me/joinchat/VRSmq`
    `!join|webamoozir`
    `+-------------------------------+`
    🔰**__leave :__**  `!leave|link or id`
    example:
    `!leave|https://t.me/joinchat/VRSmq`
    `!leave|webamoozir`
    `+-------------------------------+`
    🔰**__add to blacklist :__**  `!addword|word`
    example:
    `!addword|bet`
    `!addword|gamble`
    `+-------------------------------+`
    🔰**__show blacklist :__**  `!blacklist`
    example:
    `!blacklist`
    `+-------------------------------+`
    🔰**__remove from blacklist :__**  `!rmword|word`
    example:
    `!rmword|bet`
    `!rmword|gamble`
    `+-------------------------------+`
    🔰**__show Links :__**  `!links`
    example:
    `!links`
    `+-------------------------------+
```
