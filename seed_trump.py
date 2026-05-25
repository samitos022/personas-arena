"""
Seed script: creates Donald Trump character + 10 approved questions with real answers
extracted from the Lex Fridman Podcast #442 transcript.
"""
from database import engine
from models import Base, Character, Question
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

QUESTIONS = [
    {
        "text": "What drives you more, the love of winning or the hate of losing?",
        "real_answer": (
            "Maybe equally, maybe both. I don't like losing and I do like winning. "
            "I've never thought of it as to which is more of a driving force. "
            "The great champions have something very different. Talent wise, sometimes "
            "you can't tell the difference in talent. But at the end of a weekend, they "
            "seem to win and it's very interesting. The one thing I would say that "
            "everybody seems to have in common is they're very driven. They're driven beyond."
        ),
    },
    {
        "text": "Politics is a dirty game — how do you win at it?",
        "real_answer": (
            "Well, you win at that game by getting the word out and by using sense. "
            "You have to have a feeling where it's going. You also have to have a feeling "
            "of what's right. You can't necessarily just go what's popular, you have to do "
            "what's good for a country. But you have to get the word out and you have to "
            "just continuously get on these platforms. I did Spaces with Elon and they got "
            "numbers like nobody's ever heard before. You wouldn't do those numbers on radio, "
            "you wouldn't do them on television."
        ),
    },
    {
        "text": "What is the difference between achieving success in business versus politics?",
        "real_answer": (
            "They're different, very different. I have a lot of people that are in business "
            "that are successful and they'd like to go over to politics and then you realize "
            "they can't speak, they choke. It's hard to make a speech in front of a big "
            "audience. For many people it's virtually impossible to get up and speak for an "
            "hour and a half and have nobody leave. It's not an easy thing to do and it's "
            "an ability. There are many people in business right now, very well known, but "
            "it takes guts to run. For president, I can tell you it takes guts to run. "
            "It's a very dangerous profession, but it takes a lot of courage."
        ),
    },
    {
        "text": "You've said you could end the war in Ukraine. What would that deal look like?",
        "real_answer": (
            "I think the deal — and I wouldn't talk about it too much because I think I can "
            "make a deal if I win — I'll have a deal made guaranteed. That's a war that "
            "shouldn't have happened. It's terrible. It's a much tougher deal to make than "
            "it would've been before it started. Millions of people — I think the death "
            "numbers are going to be a lot higher than people think. They lie about the numbers. "
            "They try and keep them low. That's a war that absolutely has to get done. "
            "Ukraine is being demolished. They're destroying a great culture."
        ),
    },
    {
        "text": "In high-stakes negotiations, what works better — friendship and the carrot, or threats and the stick?",
        "real_answer": (
            "So it depends on who the person is. Everyone's different. Negotiation is "
            "interesting because it depends on who the person is. And then you have to guess "
            "or know through certain knowledge which is more important, the carrot or the "
            "stick. And with some people, it's the stick. And with some people, it's the carrot. "
            "I think the stick probably is generally more successful when we're talking about war. "
            "In Afghanistan, that was the stick, definitely the stick. The threat of military force."
        ),
    },
    {
        "text": "How do you think we should solve the immigration crisis at the border?",
        "real_answer": (
            "You've got to get the criminals out of here fast, right? The people from mental "
            "institutions, you've got to get them back into their mental institutions. No country "
            "can afford this. It's just too much money. There's no country that can afford this. "
            "We can't afford it, and we've got to get the bad ones out immediately and the rest "
            "have to be worked on. I had it fixed. I had the lowest number that we've ever had "
            "come into our country in recorded history, and we have to get it back to that again."
        ),
    },
    {
        "text": "You were the most powerful man in the world as president. Does power threaten to corrupt you?",
        "real_answer": (
            "No, I don't think so. Look, I've been there for four years. I could have done a "
            "big number on Hillary Clinton. I thought it looked terrible to take the president's "
            "wife and put her in prison. She's so lucky I didn't do anything. I thought it looked "
            "so bad. I didn't want to put her in jail and I didn't. I explained it to people — "
            "they said 'Lock her up.' I said, 'We don't want to put her in jail. We want to bring "
            "the country together.' And then when I got out, they went to work on me. They suffer "
            "from massive Trump derangement syndrome, TDS, and I don't know if it's curable."
        ),
    },
    {
        "text": "What is your policy on marijuana legalization?",
        "real_answer": (
            "First of all, medical marijuana has been amazing. I've had friends and I've had others "
            "and doctors telling me that it's been absolutely amazing. And we put out a statement "
            "that we can live with the marijuana. It's got to be a certain age to buy it. It's got "
            "to be done in a very concerted, lawful way. You go into some of these places, like in "
            "New York, it smells all marijuana. You've got to have a system where there's control. "
            "I think the way they've done it in Florida is very good."
        ),
    },
    {
        "text": "How often do you think about your own death? Are you afraid of it?",
        "real_answer": (
            "I have a friend who's very successful, in his mid 80s, and he starts off the "
            "conversation going, 'Tick tock, tick tock.' This is a dark person in a sense, but "
            "it is what it is. If you're religious, you have I think a better feeling toward it. "
            "You're supposed to go to heaven, ideally, not hell, if you're good. I think our "
            "country's missing a lot of religion. I think it really was a much better place with "
            "religion. Without religion there are no guardrails. I'd love to see us get back to "
            "more religion in this country."
        ),
    },
    {
        "text": "When you post on Truth Social, are you ever being intentionally provocative, and do you ever regret what you post?",
        "real_answer": (
            "Yeah, I do, but not that often, honestly. I do a lot of re-posting. The ones you "
            "get in trouble with are the re-posts, because you find down deep they're into some "
            "group that you're not supposed to be re-posting. You don't even know if those groups "
            "are good, bad or indifferent. But the re-posts are the ones that really get you in "
            "trouble. When you do your own words, it's sort of easier. Truth is very powerful. "
            "It's my platform and it's been very powerful, very, very powerful. I call it my typewriter."
        ),
    },
]


def seed():
    with Session(engine) as db:
        # Create or get character
        char = db.query(Character).filter(Character.slug == "donald-trump").first()
        if not char:
            char = Character(name="Donald Trump", slug="donald-trump", created_by="sam")
            db.add(char)
            db.flush()
            print(f"Created character: Donald Trump (id={char.id})")
        else:
            print(f"Character already exists: Donald Trump (id={char.id})")

        added = 0
        for q_data in QUESTIONS:
            existing = db.query(Question).filter(
                Question.character_id == char.id,
                Question.text == q_data["text"],
            ).first()
            if existing:
                print(f"  SKIP (exists): {q_data['text'][:60]}...")
                continue

            q = Question(
                character_id=char.id,
                text=q_data["text"],
                real_answer=q_data["real_answer"],
                added_by="sam",
                approved=True,
            )
            db.add(q)
            added += 1
            print(f"  ADD: {q_data['text'][:60]}...")

        db.commit()
        print(f"\nDone. Added {added} questions to character '{char.name}' (id={char.id}).")


if __name__ == "__main__":
    seed()
