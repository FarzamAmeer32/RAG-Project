

from flask import Flask, render_template, request, jsonify
from RAG.pipeline import build_rag_pipeline, rag_pipeline


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# BUILD RAG PIPELINE
# ============================================================

print("=" * 60)
print("BUILDING RAG PIPELINE")
print("=" * 60)

collection = build_rag_pipeline()

print("=" * 60)
print("RAG PIPELINE READY")
print("=" * 60)

print("ChromaDB documents:", collection.count())


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# ASK QUESTION
# ============================================================

@app.route("/ask", methods=["POST"])
def ask_question():

    try:

        # Get JSON data from frontend
        data = request.get_json()

        # Get question
        question = data.get("question", "").strip()

        # Check empty question
        if not question:

            return jsonify({
                "error": "Please enter a question."
            }), 400


        print("\n" + "=" * 60)
        print("NEW QUESTION")
        print("=" * 60)

        print("Question:", question)


        # Run complete RAG pipeline
        result = rag_pipeline(
            question,
            collection
        )


        print("\nAnswer generated successfully.")


        # Return result to frontend
        return jsonify({

            "answer": result["answer"],

            "sources": result["sources"]

        })


    except Exception as e:

        print("\nERROR:")
        print(e)

        return jsonify({

            "error": str(e)

        }), 500


# ============================================================
# RUN FLASK
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )

