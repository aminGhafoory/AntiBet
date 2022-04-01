# AntiBet
![stop](https://raw.githubusercontent.com/aminGhafoory/AntiBet/main/stop.jpeg?token=GHSAT0AAAAAABSTKY5OFEWUJQASROJW4NX4YSG6CJA)
## How To USe
1. visit [telegram](https://my.telegram.org/auth?to=apps) website and get a api-hash and api-key
2. Replace api_id and api_hash values with your own in `config.ini` file (without quotes).
3. run this command `$ chmod +x wrapper.sh`(in linux machine or WSL)
4. run this command and login to your  telegram account`$ ./wrapper.sh`
5. you can use this application just like this but if you want to dockerize it follow next steps
6. build an image with all of newly generated files using this command `docker build -t antibet:latest .`
7. now you can run your own containers;
8. use this command for running a container`docker run -d -p 8000:8000 antibet:latest`
9. this app will make an api for accessing gatherd link in `localhost:8000/links` 
10. have fun 🎈 
