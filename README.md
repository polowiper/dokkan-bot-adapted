# Dokkan Bot
This is based on the work of Tanukijs and FlashChaser and his team (source code available at https://github.com/tanukijs/dokkan-bot/tree/dev).

This is a very minimal way to use dokkan's WT API and most of the code has simply been erased. To find an actual working bot please refer to the original repo.

### Usage

First please make sure that you have every dependencies installed for that just do

`pip install -r requirements.txt`

or for nix users

`nix develop`

As said you will need an account to do that you can simply use the main file
`cd src && python main.py`


Once you have a dokkan account setup just use the fetch file `cd src && python fetch.py`

### Config

Inside the `fetch.py` files there are multiple options you can modify

- **ACCOUNT**: This must be the name of the account you just setup
- **FETCH_SZ**: This is the sample size of players that you will fetch during each fetch the minimum is 100 and you cannot do more players that there are players in the wt ofc
- **WT_EDITION**: As the name suggests this must be the current edition of the wt you're looking at (although this works on older wt as well but gives weird results)
- **DELAY**: This is the delay (in minutes) that there will be between each fetch
- **SAVE_PATH**: You can use this to send the fetches directly to your own copy of the [DokkanWTBot](https://github.com/polowiper/DokkanWTBot) for example
