# PostApi
PostApi is a program that allows the user to connect to various social media accounts and afterwards post content on these accounts. This tool should make it simpler to gather all of the different accounts in one place in order to make a clean management possible.

## Website
The Website is in a early stage of development. There still will be added some things during the development of PostApi.

## How it works
The plan is to make it connect to the different APIs that social media platforms offer and let the user publish content on these via PostApi. There will be a detailed documentation once one platform support is finished.

### Instagram
This is a tricky to be honest. I had to trick the Graph API into posting, because the Graph API needs the picture or video to be in the Internet and not a locale file. So I created a Github Account with a repo where the Program will upload the pictures and then PostAPI sents the post request with a link pointing at the github content. I know its not the best way, but for someone, who doesn't own a domain or website, is this a proper way to still post on Instagram.

## Planned Support for these Social Media Platforms
### Tiktok
I will continue the development of Tiktok support, after I finished the first Version of the UI and when Instagram-Posting is working properly via the UI.

### Instagram
Im working on Instagram at the moment.

### Facebook?
### Youtube?
### Other?
If you know any Social Media Platform that PostApi should support, then please contact me and I'll work on it.

## Data
This Tool will not be sending any data to the creator(s) of this tool. The only thing it will store are API-Keys and API-Secrets (thats the plan) in a encrypted .env file. At the moment the .env files are not encrypted, but I got another idea. I will create a docker server instance, that stores the api keys and also can be used to post content. It also can only be used to store the api-key and then post via the program.

## Note
Note that this tool is still 'Work in Progress' and I'll try to work on it as much as possible.
Note also that you are free to contribute to this project and if you do so i would be happy if u contact me. Prohibited is, that you download this project and republish is it in your name.