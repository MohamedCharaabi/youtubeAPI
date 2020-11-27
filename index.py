from flask import Flask, jsonify, request
import youtube_dl
import pafy

app = Flask(__name__)

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
    mp4format = []
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
        mp4Quality = ["394", "395", "396", "397", "398", "399"]

        for z in urls:
            a = z["format_id"]
            if a == "140":
                audioFormat.append(z)

            if a in mp4Quality:
                mp4format.append(z)

    return jsonify({"data": {"title": title, "mp4": mp4format, "audio": audioFormat}})


if __name__ == '__main__':

    app.run(debug=True)
