from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime, timedelta, timezone

# ---------------- CONFIG ----------------

API_KEY = "AIzaSyB-zPS_3JHR-6XyYqa9xaJRys_vfaueG2A"

CHANNELS = [
    "UCA-mWX9CvCTVFWRMb9bKc9w"
]

youtube = build("youtube", "v3", developerKey=API_KEY)

# ---------------- FUNCTIONS ----------------

def get_recent_videos(channel_id):
    time_limit = datetime.now(timezone.utc) - timedelta(hours=72)

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=10,
        type="video"
    )

    response = request.execute()

    videos = []

    for item in response.get("items", []):
        try:
            published = item["snippet"]["publishedAt"]
            published_time = datetime.fromisoformat(
                published.replace("Z", "+00:00")
            )

            if published_time >= time_limit:
                video_id = item["id"]["videoId"]
                videos.append(video_id)

        except:
            continue

    return videos


def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        text = " ".join([t["text"] for t in transcript])

        return text

    except:
        return None


def summarize(text):
    sentences = text.split(".")

    return ". ".join(sentences[:5]) + "..."


# ---------------- MAIN ----------------

for channel in CHANNELS:

    videos = get_recent_videos(channel)

    for vid in videos:

        transcript = get_transcript(vid)

        if transcript:

            summary = summarize(transcript)

            filename = f"{vid}.txt"

            with open(filename, "w", encoding="utf-8") as f:

                f.write("VIDEO ID:\n")
                f.write(vid + "\n\n")

                f.write("SUMMARY:\n")
                f.write(summary)

            print("Saved:", filename)

print("Done")
