from flask import Flask, request, jsonify, render_template
from config import Config
from extensions import db
from models import Book


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app


app = create_app()


# ---------- FRONTEND ----------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# ---------- CREATE ----------
@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json(silent=True) or {}

    # Basic validation
    if not data.get("title") or not data.get("author"):
        return jsonify({"error": "title and author are required"}), 400

    total_copies = data.get("total_copies", 1)

    book = Book(
        title=data["title"],
        author=data["author"],
        genre=data.get("genre"),
        isbn=data.get("isbn"),
        total_copies=total_copies,
        available_copies=data.get("available_copies", total_copies),
    )

    db.session.add(book)
    db.session.commit()

    return jsonify(book.to_dict()), 201


# ---------- READ (list + filter) ----------
@app.route("/books", methods=["GET"])
def get_books():
    query = Book.query

    author = request.args.get("author")
    genre = request.args.get("genre")

    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))

    books = query.order_by(Book.id).all()
    return jsonify([b.to_dict() for b in books]), 200


# ---------- READ (single) ----------
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict()), 200


# ---------- UPDATE ----------
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json(silent=True) or {}

    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.genre = data.get("genre", book.genre)
    book.isbn = data.get("isbn", book.isbn)
    book.total_copies = data.get("total_copies", book.total_copies)
    book.available_copies = data.get("available_copies", book.available_copies)

    db.session.commit()
    return jsonify(book.to_dict()), 200


# ---------- DELETE ----------
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"Book {book_id} deleted"}), 200


# ---------- BORROW (business logic on top of CRUD) ----------
@app.route("/books/<int:book_id>/borrow", methods=["PATCH"])
def borrow_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if book.available_copies <= 0:
        return jsonify({"error": "No copies available to borrow"}), 400

    book.available_copies -= 1
    db.session.commit()
    return jsonify(book.to_dict()), 200


# ---------- RETURN ----------
@app.route("/books/<int:book_id>/return", methods=["PATCH"])
def return_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if book.available_copies >= book.total_copies:
        return jsonify({"error": "All copies are already returned"}), 400

    book.available_copies += 1
    db.session.commit()
    return jsonify(book.to_dict()), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "library-api"
    }), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run()