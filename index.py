from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box_number = Column(Integer, default=0)


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False', echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

while True:
    print("1. Add flashcards\n2. Practice flashcards\n3. Exit")
    choice = input()
    if choice == '1':
        while True:
            print("1. Add a new flashcard\n2. Exit")
            choice = input()
            if choice == '1':
                while True:
                    print("\nQuestion:")
                    question = input()
                    if question and question.count(" ") != len(question):
                        break
                while True:
                    print("Answer:")
                    answer = input()
                    if answer and answer.count(" ") != len(answer):
                        break
                new_data = Flashcard(question=question, answer=answer)
                session.add(new_data)
                session.commit()
            elif choice == '2':
                break
            else:
                print(f"{choice} is not an option")
    elif choice == '2':
        flashcards_query = session.query(Flashcard)
        if flashcards_query.count() > 0:
            for flashcard in flashcards_query.all():
                while True:
                    print(f"Question: {flashcard.question}")
                    print('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:')
                    choice = input()
                    if choice in ("y", "n", "u"):
                        break
                    print(f"{choice} is not an option")
                if choice == 'y':
                    print(f"Answer: {flashcard.answer}")
                    while True:
                        choice = input('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n')
                        if choice in ("y", "n"):
                            break
                        print(f"{choice} is not an option")
                    if choice == "y":
                        flashcards_query.filter(Flashcard.id == flashcard.id) \
                            .update({"box_number": Flashcard.box_number + 1})
                        session.commit()
                        if flashcard.box_number == 3:
                            flashcards_query.filter(Flashcard.id == flashcard.id).delete()
                            session.commit()
                    else:
                        flashcards_query.filter(Flashcard.id == flashcard.id) \
                            .update({"box_number": 0})
                        session.commit()
                elif choice == 'u':
                    choice = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n')
                    if choice == 'd':
                        flashcards_query.filter(Flashcard.id == flashcard.id).delete()
                        session.commit()
                    elif choice == 'e':
                        question = input(f"current question: {flashcard.question}\nplease write a new question:\n")
                        answer = input(f"current answer: {flashcard.answer}\nplease write a new answer:\n")

                        if (question and question.count(" ") != len(question)) \
                                and (answer and answer.count(" ") != len(answer)):
                            flashcards_query.filter(Flashcard.id == flashcard.id)\
                                .update({"question": question, "answer": answer})
                            session.commit()

                elif choice == 'n':
                    continue
                else:
                    print(f"{choice} is not an option")
        else:
            print("There is no flashcard to practice!\n")
    elif choice == '3':
        print("Bye!")
        break
    else:
        print(f"{choice} is not an option")
