import jiosaavn

# Initialize the client
client = jiosaavn.Sync()

# Get song details using a JioSaavn song URL
song_url = "https://www.jiosaavn.com/song/tum-hi-ho/XYZ123"  # Replace with actual link
song = client.get_song(song_url)

print(song)
print(dir(jiosaavn))

PORT = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
