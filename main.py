from website import create_app

app = create_app()
# https://www.youtube.com/watch?v=dam0GPOAvVI&t=151s
if __name__ == '__main__':
    app.run(debug=True)