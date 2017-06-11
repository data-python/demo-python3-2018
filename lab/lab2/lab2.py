#
import twitter
consumer_key = "<Your Consumer Key Here>"
consumer_secret = "<Your Consumer Secret Here>"
access_token = "<Your Access Token Here>"
access_token_secret = "<Your Access Token Secret Here>"
authorization = twitter.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
import os
output_filename = os.path.join(os.path.expanduser("~"),   "Data", "twitter", "python_tweets.json")
import json
t = twitter.Twitter(auth=authorization)
with open(output_filename, 'a') as output_file:
	search_results = t.search.tweets(q="python", count=100)['statuses']
	for tweet in search_results:
		if 'text' in tweet:
			output_file.write(json.dumps(tweet))
			output_file.write("\n\n")


# 加载数据集并对其分类
tweet_sample = tweets
labels = []
if os.path.exists(classes_filename):
    with open(classes_filename) as inf:
        labels = json.load(inf)

def get_tweet():
    return tweet_sample[len(labels)]['text']

%%html
<div name='tweetbox'>
    Instructions: Click in test box. Enter a 1 if the tweet is relevant, enter 0 otherwise. <br>
    Tweet: <div id="tweet_text" value='text'></div> <br>
    <input type="text" id="capture"> <br>
</div>

<script>
    function set_label(label) {
        var kernel = IPython.notebook.kernel;
        kernel.execute('labels.append(' + label + ')');
        load_next_tweet();
    }

   function load_next_tweet() {
        console.log('1');
        var code_input = 'get_tweet()';
        console.log('2');
        var kernel = IPython.notebook.kernel;
        console.log("3");
        var callbacks = { 'iopub' : {'output' : handle_output}};
        console.log("4");
        kernel.execute(code_input, callbacks, {silent:false});
        console.log("5");
    }


    $("input#capture").keypress(function(e) {
        console.log(e);
        if(e.which == 48) {
            // 0 pressed
            set_label(0);
            $("input#capture").val("");
        } else if(e.which == 49) {
            // 1 pressed
            set_label(1);
            $("input#capture").val("");
        }
    })
    load_next_tweet();
</script>

with open(labels_filename, 'w') as outf:
	json.dump(labels, outf)
