# Chatbot Engine

This is a demo of a multi-lingual chatbot powered by [Rasa](https://rasa.com/). 
The entire app runs on a single web server, which makes it easy to deploy and maintain it at low cost.

The demo runs on Heroku, feel free to [try it out](https://chatbot-engine-web.herokuapp.com/)!

## Features
- Supports multiple models and languages
- Easy to spin up (Docker) and deploy (automated CI)  
- Makes it easy to build your own model (training, interactive learning, custom actions)
- Continuously updated to run on the latest Rasa stack 

## How to ..

### Start it on your local machine
`docker-compose up`

Please note it might take longer the first time for the server to start. There are many dependencies that need to be downloaded. Subsequent starts are gonna be quick though.

### Train your model
`./server.sh train [de|en|sv]`
`./server.sh train ./examples/coffee_bot en`

### Run using MacOS Terminal (Python 3.6.9)
`conda activate rasa`
`cd examples/rasa_bot`

`pip install "rasa[transformers]`

`rasa train --config ./config/models/en/config.yml --domain ./config/models/en/domain.yml --data ./config/models/en/data --out "./models" --fixed-model-name "chat-model-en"`

`rasa run actions --actions actions.actions`

`python3 app.py`



The script process training data stored in `config/models` and stores the output in the `models` directory.

Currently only three languages are supported, but it's easy to completely change them or add more.
In fact, given the simplicity of the model in the demo, it can be trained for any language you like, as long as it's supported by Rasa NLU. See [supervised embeddings](https://rasa.com/docs/rasa/nlu/choosing-a-pipeline/#supervised-embeddings).
You can also change the [NLP pipeline](https://rasa.com/docs/rasa/nlu/choosing-a-pipeline) as you please.

### Add a custom action
Either amend the [actions.py](examples/rasa_demo/actions/actions.py) script or drop a new script to the [actions](examples/rasa_demo/actions) module.

### Write your model from scratch
Drop a new model config in the [models](examples/rasa_demo/config/models) directory. Have a look at the existing examples.

## Architecture

Rasa provides a lot of convenience. It's easy to start the core as well as the action server. Running multiple web servers can however be a problem when it comes to hosting.
Multiple web processes or communication via HTTP in a Heroku cluster is only allowed with pricier plans.

Another issue is the lack of support for multiple models in the current version of Rasa (1.6.0). Suppose you train your bot in two languages. As it stands now, you need to spin up an additional core server to serve your other model.
With a little bit of an extra effort, it is perfectly possible to enable multiple models with Rasa's SDK. Check my [BotFactory](utils/bot_factory.py) if you are interested in details.

## Attribution
- [Rasa](https://rasa.com) for providing such an awesome framework.
- [Emojious](https://www.iconfinder.com/iconsets/flags-37?utm_source=sharing-feature&utm_medium=social&utm_campaign=sharing-feature&utm_content=link) for all the amazing icons free of charge
- [Chatbots Life](https://chatbotslife.com/) for sharing invaluable insights and guidance