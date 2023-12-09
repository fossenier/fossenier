# list of movies (title, length, year)
movies = [
    ["The Holy Grail", 91, 1975],
    ["The Life of Brian", 91, 1979],
    ["The Meaning of Life", 107, 1983],
]
print([movies[i][0] for i in range(len(movies)) if movies[i][2] == 1975])
