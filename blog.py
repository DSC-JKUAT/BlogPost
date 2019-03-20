from flask import Flask, jsonify, request, make_response
from models import Blog, Validators
app = Flask(__name__)

blogs = []


@app.route('/api/v1/blog', methods=['POST'])
def create_blog():
    if 'title' not in request.json:
        return jsonify({"Message": "Title field is required"}), 400
    if 'content' not in request.json:
        return jsonify({"Message": "Content field is required"}), 400

    title = request.json['title']
    content = request.json['content']

    if not Validators.valid_title(title):
        return jsonify({
            "Message": "Title should be alphanumeric and be 3 to 20 characters"
        }), 400

    if not Validators.valid_content(content):
        return jsonify({
            "Message": "Content should be alphanumeric, can have special characters and be above 10 characters"
        }), 400

    newBlog = Blog(title, content)
    blogs.append(newBlog)

    return jsonify({
        "Message": "Blog created successfully",
        "blog": newBlog.__dict__
    }), 201


@app.route('/api/v1/blog', methods=['GET'])
def get_all_blogs():
    all_blogs = [blog.__dict__ for blog in blogs]
    if len(all_blogs) == 0:
        return jsonify({"Message": "There are no blogs for now"}), 404
    return jsonify({"Blogs": all_blogs}), 200


@app.route('/api/v1/blog/<int:blog_id>', methods=['GET'])
def get_specific_blog(blog_id):
    blog = [blog.__dict__ for blog in blogs if blog.id == blog_id]
    if not blog:
        return jsonify({"Message": "There is no blog with that id"}), 404
    return jsonify({"Blog": blog[0]}), 200


@app.route('/api/v1/blog/<int:blog_id>', methods=['DELETE'])
def delete_specific_blog(blog_id):
    blog = [blog for blog in blogs if blog.id == blog_id]
    if not blog:
        return jsonify({"Message": "There is no blog with that id"}), 404
    blogs.remove(blog[0])
    return jsonify({"Message": "Blog deleted successfully"}), 200


@app.route('/api/v1/blog/<int:blog_id>', methods=['PUT'])
def update_specific_blog(blog_id):
    blog = [blog for blog in blogs if blog.id == blog_id]

    if not request.json:
        return jsonify({"Message": "Enter the field to be updated"}), 400

    if not blog:
        return jsonify({"Message": "There is no blog with that id"}), 404

    title = request.json['title']
    content = request.json['content']

    if not Validators.valid_title(title):
        return jsonify({
            "Message": "Title should be alphanumeric and be 3 to 20 characters"
        }), 400

    if not Validators.valid_content(content):
        return jsonify({
            "Message": "Content should be alphanumeric, can have special characters and be above 10 characters"
        }), 400

    blog[0].title = title
    blog[0].content = content

    return jsonify({
        "Message": "Blog updated successfully",
        "Updated blog": blog[0].__dict__
    }), 202


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Url not found'}), 404)


if __name__ == "__main__":
    app.run(debug=True)
