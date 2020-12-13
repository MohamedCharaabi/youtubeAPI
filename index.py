from flask import Flask, jsonify, request, render_template
import youtube_dl
from flask_material import Material

app = Flask(__name__)
app.static_folder = 'static'
Material(app)


ydl_opts = {
    'format': 'bestaudio/best',
    'keepvideo': False,
    # 'outtmpl': filename,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}
# url = 'https://www.youtube.com/watch?v=_XUllZT1gug'


@app.route('/<string:url>', methods=['GET'])
def form(url):
    # if request.method == "POST":
    videoformat = []
    audioFormat = []
    title = ""
    videoUrl = "www.youtube.com/watch?v=" + url

    with youtube_dl.YoutubeDL() as ydl:
        ydl.cache.remove()
        r = ydl.extract_info(url=videoUrl, download=False)
        # title
        title = r["title"]

        urls = r["formats"]
    #      print('the url =>', urls[0])
    #      c = urls[0]
        mp4 = [x for x in urls if x["ext"] == "mp4"]
        mp4Quality = ["395", "396", "397", "398",
                      "399", "134", "137", "22", "18"]
        mp3Quality = ["394", "140", "139"]
        formatNote = ["144p", "360p", "480p", "720p", "1080p"]

        for z in urls:
            a = z["format_id"]
            if a in mp3Quality:
                audioFormat.append(z)

            if a in mp4Quality:
                videoformat.append(z)

    return jsonify({"data": {"title": title, "mp4": videoformat, "mp3": audioFormat}})
    # return jsonify({"data": urls})


@app.route('/', methods=['GET', 'POST'])
def facebook():
    if request.method == "POST":
        videoformat = []
        audioFormat = []
        title = ""
        url = request.form.get("videoUrl")
        with youtube_dl.YoutubeDL() as ydl:
            ydl.cache.remove()
            r = ydl.extract_info(url=url, download=False)
        # title
            title = r["title"]

            urls = r["formats"]
    #      print('the url =>', urls[0])
    #      c = urls[0]
            mp4 = [x for x in urls if x["ext"] == "mp4"]
            mp4Quality = ["394", "395", "396", "397", "398",
                          "399", "134", "137", "22", "18"]
            mp3Quality = ["140", "139"]
            formatNote = ["144p", "360p", "480p", "720p", "1080p"]

            for z in urls:
                a = z["format_id"]
                if a in mp3Quality:
                    audioFormat.append(z)

                if a in mp4Quality:
                    videoformat.append(z)

        return render_template('result.html', audio=audioFormat, video=videoformat)

    return render_template('form.html')


# @app.route("/down/try/<string:video_url>", methods=['GET', 'POST'])
# def download_file(video_url):
#     video_info = youtube_dl.YoutubeDL().extract_info(
#         url='https://www.youtube.com/watch?v=JaO6fPA99Hg&t=1378s', download=False
#     )
#     filename = f"{video_info['title']}.mp3"
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'keepvideo': False,
#         'outtmpl': filename,
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(
#             'https://www.youtube.com/watch?v=JaO6fPA99Hg&t=1378s', download=False)
#         video_title = info_dict.get('title', None)
#     path = f'C:\\{video_title}.mp3'
#     ydl_opts.update({'outtmpl': path})
#     try:
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([video_url])
#     except:
#         return jsonify({"data": "ERROE"})
#     return jsonify({"data": video_title})
if __name__ == '__main__':

    app.run(debug=True)
