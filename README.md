## Notice:
***
The code in main.py:
```python
params_alreadyKnown = [0, 0, 0, 0] # set your picture's statistical params which has been alreaady known On Pixiv
```

must fix for yourself(e.g. [views on Pixiv, likes, bookmarks, num of tags, ...])
***
This code doesn't include parameters learned by regression.

You need pairs of an image and peopele's scores of the image to make this system learn.

If you will run the system, your key/url for MS Azure REST API are required. Also your patience to collect images and scores may be needed.

## Abstruct:
The purpose this system is to find stuff in pictures which lets people find them fascinating

## Method:
Pixiv is one of the most famouse illust SNS in japan.

Every work on Pixiv has feedbacks of the work from people who wathed the work as shapes like "comments", "likes", "views", and so on.

The goal of this system is make it obvious what stuff make these feedbacks high.

To achive the goal, this system tries to use 'Machine learning (object detection)' and leverage the result values as transfer learning.

The sequence is as below:

1. Get each feedbacks and image of works On Pixiv
2. Send query of each image to Ms Azure Computer vision REST API
3. Save the responses into local DB
4. Use regression for each work with parameters of (2.) as input and feedbacks of (1.) as output both correspond the work

|Images||Scores||Regression|
|:--:|:--:|:--|:--:|:--:|
|image 1|→|<span style="color: maroon; ">**People's Scores**</span>(image 1)|➡|Estimating function of <br> (<span style="color: navy; ">**Machine learning Scores**</span>) -> (<span style="color: maroon; ">**People's Scores**</span>)|
||→|<span style="color: navy; ">**Machine learning Scores**</span>(image 1)|⤴|
|||
|image 2|→|<span style="color: maroon; ">**People's Scores**</span>(image 2)|⤴|
||→|<span style="color: navy; ">**Machine learning Scores**</span>(image 2)|⤴|
|:|:|