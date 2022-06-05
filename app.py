# YouTubeTranscriptAPI Imports
from time import time
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, VideoUnavailable, TooManyRequests, \
    TranscriptsDisabled, NoTranscriptAvailable
from youtube_transcript_api.formatters import TextFormatter

# Transformers Imports
from transformers import BartTokenizer, BartForConditionalGeneration
import torch

# Flask Imports
from flask import Flask, jsonify, request
from flask_cors import CORS

import time


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index_page():
    return "Hello world"

def get_transcript(video_id):
    # Using Formatter to store and format received subtitles properly.
    formatter = TextFormatter()
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    formatted_text = formatter.format_transcript(transcript).replace("\n", " ")
    return formatted_text
                        

def get_summary(transcript):
    tokenizer = BartTokenizer.from_pretrained("./models")
    model = BartForConditionalGeneration.from_pretrained("./models")
    # tokenize without truncation
    inputs_no_trunc = tokenizer(transcript, max_length=None, return_tensors='pt', truncation=False)
    chunk_start = 0
    chunk_end = tokenizer.model_max_length  # == 1024 for Bart
    inputs_batch_lst = []
    size_lst = []
    print("Tokenizing")
    while chunk_start <= len(inputs_no_trunc['input_ids'][0]):
        inputs_batch = inputs_no_trunc['input_ids'][0][chunk_start:chunk_end]  # get batch of n tokens
        inputs_batch = torch.unsqueeze(inputs_batch, 0)
        inputs_batch_lst.append(inputs_batch)
        size_lst.append(chunk_end-chunk_start)
        chunk_start += tokenizer.model_max_length  # == 1024 for Bart
        chunk_end += tokenizer.model_max_length  # == 1024 for Bart

    # generate a summary on each batch
    print("Generating Summary")
    summary_ids_lst = [model.generate(inputs, num_beams=4, min_length=size//10, max_length=1000, early_stopping=True) for inputs, size in zip(inputs_batch_lst, size_lst)]

    # decode the output and join into one string with one paragraph per summary batch
    print("Decoding output")
    summary_batch_lst = []
    for summary_id in summary_ids_lst:
        summary_batch = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_id]
        summary_batch_lst.append(summary_batch[0])
    summary_all = ' '.join(summary_batch_lst)
    return summary_all

# Processing Function for below route.
@app.route('/api/summarize/', methods=['GET'])
def transcript_fetched_query():
    start_time = time.time()
    # Getting argument from the request
    print("Starting function")
    video_id = request.args.get('id')  # video_id of the YouTube Video
    try:
        transcript = get_transcript(video_id)
        print("Transcript done")
    # Catching Exceptions
    except VideoUnavailable:
        return jsonify(success=False, message="VideoUnavailable: The video is no longer available.",
                        response=None), 400
    except TooManyRequests:
        return jsonify(success=False,
                        message="TooManyRequests: YouTube is receiving too many requests from this IP."
                                " Wait until the ban on server has been lifted.",
                        response=None), 500
    except TranscriptsDisabled:
        return jsonify(success=False, message="TranscriptsDisabled: Subtitles are disabled for this video.",
                        response=None), 400
    except NoTranscriptAvailable:
        return jsonify(success=False,
                        message="NoTranscriptAvailable: No transcripts are available for this video.",
                        response=None), 400
    except NoTranscriptFound:
        return jsonify(success=False, message="NoTranscriptAvailable: No transcripts were found.",
                        response=None), 400
    except:
        # Prevent server error by returning this message to all other un-expected errors.
        return jsonify(success=False,
                        message="Some error occurred. Contact the administrator if it is happening too frequently. Failed at get_transcript",
                        response=None), 500
    # return jsonify(success=True, message="Subtitles for this video was fetched and summarized successfully.",
    #                 response=transcript), 200
    try:
        summary = get_summary(transcript)
    except:
        # Prevent server error by returning this message to all other un-expected errors.
        return jsonify(success=False,
                        message="Some error occurred."
                                " Contact the administrator if it is happening too frequently. Failed at get_summary",
                        response=None), 500
    end = time.time()
    #print(end-start_time)
    return jsonify(success=True, message="Subtitles for this video was fetched and summarized successfully.",
                    response=summary), 200

if __name__ == '__main__':
    # Running Flask Application
    app.run()