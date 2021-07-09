from .models import Test
from questions.models import Question, Answer
import docx

def handle_uploaded_file(f,pk):
    test_pk = pk
    print('test_pk:',test_pk)
    doc = docx.Document(f)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    for question_no in range(len(fullText)):
        question_set = fullText[question_no].split(',')
        print('question_set: ',question_set)
        question = question_set[0]
        if question=='':
            continue
        question_instance = Question.objects.create(test=test_pk, text=question)
        question_instance.save()
        print('question:',question)
        for count in range(1,5):
            answer = question_set[count]
            if count == 1:
                answer_instance = Answer.objects.create(question=Question.objects.get(text=question, test=test_pk), text=answer, correct=True)
            else:
                answer_instance = Answer.objects.create(question=Question.objects.get(text=question, test=test_pk), text=answer)
            answer_instance.save()
