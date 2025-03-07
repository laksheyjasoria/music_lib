import jiosaavn

# Search for the song
results = jiosaavn.search("Tum Hi Ho")

# Get the first result (if available)
if results:
    song = results[0]
    print(song)
else:
    print("Song not found!")

print(song)
print(dir(jiosaavn))

PORT = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
