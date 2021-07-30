from django.urls import path, include
from graphene_django.views import GraphQLView
from quiz.schema import schema
from django.views.decorators.csrf import csrf_exempt

app_name = "quiz"

urlpatterns = [
    # graphql/
    path('', csrf_exempt( GraphQLView.as_view(graphiql=True, schema=schema))),
]

