from ruamel.yaml.comments import CommentedMap

from waltz.registry import Registry
from waltz.resources.quizzes.quiz_question import QuizQuestion
from waltz.tools import h2m, m2h


class MultipleChoiceQuestion(QuizQuestion):
    question_type = 'multiple_choice_question'

    @classmethod
    def decode_json_raw(cls, registry: Registry, data, args):
        result = QuizQuestion.decode_question_common(registry, data, args)
        result['answers'] = []
        for answer in data['answers']:
            a = CommentedMap()
            html = h2m(answer['html'])
            if args.hide_answers:
                a['possible'] = html
            else:
                if answer['weight']:
                    a['correct'] = html
                else:
                    a['wrong'] = html
                if answer['comments_html']:
                    a['comment'] = h2m(answer['comments_html'])
            result['answers'].append(a)
        return result

    @classmethod
    def encode_json_raw(cls, registry: Registry, data, args):
        result = QuizQuestion.encode_question_common(registry, data, args)
        result['answers'] = [
            {'comments_html': m2h(answer.get('comment', "")),
             'weight': 100 if 'correct' in answer else 0,
             'text': answer['correct'] if 'correct' in answer else answer['wrong'],
             'html': m2h(answer['correct'] if 'correct' in answer else answer['wrong'])}
            for answer in data['answers']]
        return result

    # TODO: upload

    def to_json(self, course, resource_id):
        result = QuizQuestion.to_json(self, course, resource_id)
        for index, answer in enumerate(self.answers):
            base = 'question[answers][{index}]'.format(index=index)
            result[base +"[answer_html]"] = self._get_first_field(answer, 'html', 'text')
            result[base +"[answer_comment_html]"] = self._get_first_field(answer, 'comments_html', 'comments')
            result[base +"[answer_weight]"] = answer['weight']
        return result