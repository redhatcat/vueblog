from app import app
from models.post import Post
from flask import abort, jsonify
from flask_jwt_extended import (
    jwt_optional,
    jwt_required,
    get_jwt_identity,
)

from webargs import fields, validate
from webargs.flaskparser import use_args

limit = 1

@app.route("/api/posts", methods=['POST'])
@jwt_optional
@use_args({
    'id': fields.String(validate=validate.Length(max=120)),
    'slug': fields.String(validate=validate.Length(max=120)),
    'after': fields.String(validate=validate.Length(max=120)),
    'since': fields.String(validate=validate.Length(max=120)),
    'tags': fields.List(fields.String(validate=validate.Length(max=24))),
})
def posts(args):
    filters = {
    }
    order_field = 'id'
    order = '-{}'.format(order_field)
    current_user = get_jwt_identity()
    if current_user is None:
        # Only our users/writers can see unpublished posts
        filters['published_at__ne'] = None

    if args.get('id'):
        filters['id'] = args.get('id')
    if args.get('slug'):
        filters['slug'] = args.get('slug')
    if args.get('after'):
        filters['id__lt'.format(order_field)] = args.get('after')
    if args.get('since'):
        filters['id__gt'.format(order_field)] = args.get('since')
        order = order_field
    if args.get('tags'):
        filters['tags__all'] = args.get('tags')
    queryset = Post.objects(**filters)
    queryset = queryset.order_by(order)
    queryset = queryset[:limit]
    items = [i.to_dict() for i in queryset]
    return jsonify(items=items)

@app.route("/api/posts/create", methods=['POST'])
@app.route("/api/posts/update", methods=['POST'])
@jwt_required
@use_args({
    'id': fields.String(validate=validate.Length(max=120)),
    'title': fields.String(required=True, validate=validate.Length(max=120)),
    'slug': fields.String(required=True, validate=validate.Length(max=120)),
    'body': fields.String(required=True, validate=validate.Length(max=10000)),
    'tags': fields.List(fields.String(validate=validate.Length(max=24))),
    'published_at': fields.DateTime(missing=None),
    'author': fields.String(validate=validate.Length(max=120))
})
def post_create(args):
    current_user = get_jwt_identity()
    username = current_user.get('username')
    if username is None:
        abort(403)
    post_id = args.get('id')

    # Initialize post if new
    post = None
    if post_id:
        post = Post.objects(id=post_id).first()
        if post is None:
            abort(404)
    else:
        post = Post()

    post.title = args.get('title')
    post.slug = args.get('slug')
    post.body = args.get('body')
    post.tags = args.get('tags')
    post.published_at = args.get('published_at')
    post.author = args.get('author') or username
    post.save()
    return jsonify(post.to_dict())

@app.route("/api/posts/delete", methods=['POST'])
@jwt_required
@use_args({
    'id': fields.String(required=True, validate=validate.Length(max=120)),
})
def post_delete(args):
    current_user = get_jwt_identity()
    username = current_user.get('username')
    if username is None:
        abort(403)
    post_id = args.get('id')
    post = Post.objects(id=post_id).first()
    if post is None:
        abort(404)
    response = jsonify(post.to_dict())
    post.delete()
    return response
