
# Import libraries 
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

from transformers import pipeline

url = "https://www.youtube.com/watch?v=Yiaatr-Noh0"
video_id = url.split("=")[1]
# print(video_id)

# Must be a single transcript.
transcript = YouTubeTranscriptApi.get_transcript(video_id)

formatter = JSONFormatter()

# .format_transcript(transcript) turns the transcript into a JSON string.
json_formatted = formatter.format_transcript(transcript, indent = 2)


# Now we can write it out to a file.
# Now, a new JSON file that you can easily read back into Python.

with open('youtube_transcript.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_formatted)

# text is generated and stored it into r
result = ""
for i in transcript:
    result += ' ' + i['text']
# print(result)
print(len(result))



# # using pipeline API for summarization task
summarization = pipeline("summarization")
# original_text = result

num_iters = int(len(result)/1000)
summarized_text = []
for i in range(0, num_iters + 1):
  start = 0
  start = i * 1000
  end = (i + 1) * 1000
  # print("input text \n" + result[start:end])
  out = summarization(result[start:end])
  out = out[0]
  out = out['summary_text']
  # print("Summarized text\n"+out)
  summarized_text.append(out)

#print(summarized_text)

# summary_text = summarization(original_text)[0]['summary_text']
print(str(summarized_text))
print(len(summarized_text))





# from transformers import T5ForConditionalGeneration, T5Tokenizer

# # initialize the model architecture and weights
# model = T5ForConditionalGeneration.from_pretrained("t5-base")
# # initialize the model tokenizer
# tokenizer = T5Tokenizer.from_pretrained("t5-base")

# article = result

# # encode the text into tensor of integers using the appropriate tokenizer
# inputs = tokenizer.encode("summarize: " + article, return_tensors="pt", max_length=512, truncation=True)

# # generate the summarization output
# outputs = model.generate(
#     inputs, 
#     max_length=250, 
#     min_length=40, 
#     length_penalty=5.0, 
#     num_beams=4, 
#     early_stopping=True)
# # just for debugging
# print(outputs)
# print(tokenizer.decode(outputs[0]))












