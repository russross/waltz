from ruamel.yaml.comments import CommentedMap

from waltz.registry import Registry
from waltz.resources.quizzes.quiz_question import QuizQuestion
from waltz.tools import h2m


class TextOnlyQuestion(QuizQuestion):
    question_type = 'text_only_question'

    @classmethod
    def decode_json_raw(cls, registry: Registry, data, args):
        return QuizQuestion.decode_question_common(registry, data, args)

    @classmethod
    def encode_json_raw(cls, registry: Registry, data, args):
        return QuizQuestion.encode_question_common(registry, data, args)

    # TODO: upload

    def to_json(self, course, resource_id):
        return QuizQuestion.to_json(self, course, resource_id)