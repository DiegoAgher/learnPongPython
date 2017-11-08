# learnPongPython
This project that aims to build a model that learns how to play pong using python2.7

# Requirements
Create a virtualenv that uses python2.7 along with `pip`

run `pip install -r requirements.txt`

# How to train my model and play against him?
After installing the proper requirements.
1. Gather data: run `python pong2player.py` use the up/down keys for player
on the right, and w/s for player on the left. To save the data one will have to
loose after 4 points.

2. Train your model: train an elasticnet or 2Dconvolutional Network by running
`python -m training.elasticnet` or `python -m training.conv_model_keras.py`. This
could take quite a while. Keep in mind you'll need considerable data so play
three games at least.

3. Deploy the model an play against it: run `python self_pong.py` and play 
against the player on the left. Have fun! (Disclaimer: depending on the human 
player's performance, on the left, that's how good the AI will be.

