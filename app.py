from website import create_app

# Run Server
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=2024)