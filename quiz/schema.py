from django.contrib.admin.decorators import register
from django.contrib.auth import update_session_auth_hash
import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from .models import Category, Quizzes, Question, Answer
from graphql_auth import mutations


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id","name")

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id","title","category")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title","quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question","answer_text")


class Query(UserQuery, MeQuery, graphene.ObjectType):

    all_categorys = graphene.List(CategoryType)
    all_quizzes = graphene.List(QuizzesType, category_id=graphene.Int())
    all_question = graphene.Field(QuestionType, quiz_id=graphene.Int())
    all_answers = graphene.List(AnswerType, quesntion_id=graphene.Int())

    def resolve_all_categorys(root, info):
        return Category.objects.all()

    def resolve_all_quizzes(root, info, category_id):
        return Quizzes.objects.filter(category=category_id)

    def resolve_all_question(root, info, quiz_id):
        return Question.objects.filter(quiz=quiz_id)

    def resolve_all_answers(root, info, quesntion_id):
        return Answer.objects.filter(question=quesntion_id)

class CategoryCreate(graphene.Mutation):
    class Arguments:
        name = graphene.String()
    
    category = graphene.Field(CategoryType)

    def mutate(self, info, name):
        category = Category.objects.create(name=name)
        return CategoryCreate(category=category)


class CategoryUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryUpdate(category=category)

class CategoryDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        category.delete()
        return cls(message=f"Category ID:{id} is deleted!")

class Mutation(AuthMutation ,graphene.ObjectType):
    create_category = CategoryCreate.Field()
    update_category = CategoryUpdate.Field()
    delete_category = CategoryDelete.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)