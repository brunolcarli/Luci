<table align="center"><tr><td align="center" width="9999">

<img src="https://images.generated.photos/jqguEfsi0Q7fghDlnuQ-KPkFkalSLGNHcgTIBMLVMyw/rs:fit:512:512/Z3M6Ly9nZW5lcmF0/ZWQtcGhvdG9zL3Yz/XzA5MTU5MzkuanBn.jpg" align="center" width="170" alt="Project icon">

# LUCI

*Logical Unit for Communicational Interactivity*

</td></tr>

</table>    

<div align="center">

> [![Version badge](https://img.shields.io/badge/version-0.2.2-silver.svg)](https://lisa--brunolcarli.repl.co/graphql/?query=query%7B%0A%09lisa%0A%7D)
[![Docs Link](https://badgen.net/badge/docs/github_wiki?icon=github)](https://github.com/brunolcarli/Luci/wiki)
[![test badge](https://img.shields.io/badge/test-passing-green.svg)](https://lisa--brunolcarli.repl.co/graphql/?query=query%7B%0A%09lisa%0A%7D)

LUCI is a conversational tamabotchi for discord.

</div>


## Developers

### Cloning and executing

![Linux Badge](https://img.shields.io/badge/OS-Linux-black.svg)
![Apple badge](https://badgen.net/badge/OS/OSX/:color?icon=apple)


#### Local machine


Clone this project and engage a **python3** virtual environment the way as you like and install the requirements through Makefile.

Example using virtualevwrapper:

```
$ git clone https://github.com/brunolcarli/Luci.git
$ cd luci/
$ mkvirtualenv Luci
$ (Luci) make install
```


Create a `.env` file and add the following content:

```
TOKEN=<your_test_bot_token>
LISA_URL=<lisa_url>
BACKEND_URL=None
SETTINGS_MODULE=development
REDIS_HOST=<redis_server_host>
REDIS_HOST=<redis_server_port>
```

You should configure your own environment cloning both lisa and bot api:

- `LISA_URl` is required since the bot requests text offense and sentiment to the service API.

- `BACKEND_URL` is the long range memory storage (AKA database) which is a separated service.

- `REDIS_HOST` and `REDIS_PORT` is the short term memory, and it depends on a redis-server.

Note: If `SETTINGS_MODULE=production` the bot will run on a flask server instance.

Execute the bot:

```
$ (Luci) make run
```

### Training Models

The bot is trained over a serie of .`json` datasets on `core/training/json/intentions/`.

For each intention directory there are located a serie of `dataset_x.json` where `x` is a sequence number of the train dataset. You can create a new one containing the text and training target label on the following shape:

```json
[
    {"text": "An example text.", "intention": 1},
    {"text": "Another example text.", "intention": 1},
    {"text": "Way othe example text.", "intention": 2},
    {"text": "keep going.", "intention": 2}
]
```

The training data **must** respect the intention archicture proposed on the docs, otherwise it may cause the model to behave unproperly.

Train data through Makefile:

```
$ (Luci) make train
```

You can view some models score and the number o sample data used for each intention through a cvross validation test:


```
$ (Luci) make no_free_lunch
```

### Test the bot

The goal is give the models enough data to pass the test when executing:


```
$ (Luci) make test
```


## Docker


<div align="center">

<img src="https://git.infra-lab.xyz/uploads/-/system/project/avatar/46/docker-gif-4.gif?width=64" align="center" width="170" alt="Project icon">

</div>

Set up the `.env` file as described above and build the container with docker-compose:

```
$ docker-compose build
```

Run with:

```
$ docker-compose up
```

Or run in background

```
$ docker-compose up -d
```
