"""
Seed script: creates Taylor Swift character + 10 approved questions with real answers.
Sources: Rolling Stone, New York Times, Billboard, TIME, NME, Variety, Deseret News,
         GQ, Entertainment Weekly, SiriusXM interviews (2019–2026).
"""
from database import engine
from models import Base, Character, Question
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

QUESTIONS = [
    {
        "text": "How do songs typically begin for you?",
        "real_answer": (
            "There are so many different ways that a song begins in my world. "
            "Sometimes it floats down like a cloud in front of you, and all you have to do "
            "is grab it, and the song transpires from there. That's the way it happens most "
            "of the time. But it's still such a mystery to me. Even though I've been writing "
            "songs for so long, and I've started songs and finished songs so many different "
            "ways. It's ever-changing."
        ),
    },
    {
        "text": "What was the inspiration behind creating Folklore during the pandemic?",
        "real_answer": (
            "In isolation, my imagination has run wild and this album is the result, a "
            "collection of songs and stories that flowed like a stream of consciousness. "
            "Consuming other people's art and storytelling sort of opened this portal in my "
            "imagination. I was watching films like Pan's Labyrinth, L.A. Confidential, and "
            "Rear Window during lockdown, and it freed myself up to do that from a narrative "
            "standpoint. I created characters and intersecting storylines rather than my "
            "typical autobiographical approach. If there's chaos everywhere, why not just "
            "use the damn word I want to use in the song?"
        ),
    },
    {
        "text": "You've said you organize your lyrics into three pen-themed categories. Can you explain them?",
        "real_answer": (
            "I've secretly established genre categories for lyrics I write — three of them, "
            "to be exact. They are affectionately titled Quill Lyrics, Fountain Pen Lyrics, "
            "and Glitter Gel Pen Lyrics. Quill lyrics have words and phrasings that are "
            "antiquated — if my lyrics sound like a letter written by Emily Dickinson's "
            "great-grandmother while sewing a lace curtain, that's me writing in the Quill "
            "genre. Most of my lyrics fall into the Fountain Pen category, which combines "
            "a modern storyline with a poetic twist. Glitter Gel Pen lyrics are frivolous, "
            "carefree, bouncy — they don't take themselves seriously, they're the drunk girl "
            "at the party who tells you that you look like an angel in the bathroom."
        ),
    },
    {
        "text": "What is a 'rant bridge' and why do you use it?",
        "real_answer": (
            "It's basically like stream of consciousness, endless pouring-out of emotion, "
            "intrusive thoughts, blended with metaphor, with discussion, with shouting. "
            "Songs like 'Out of the Woods,' 'Is It Over Now?' and 'Cruel Summer' feature "
            "rant bridges. You want this rant bridge to feel the most intense of what that "
            "feeling is that you're trying to establish over the course of the song, and you "
            "want it to kind of be a crescendo. The bridge can be where you zoom back, you "
            "walk 20 feet back, and you see what this entire painting was supposed to be."
        ),
    },
    {
        "text": "How do you keep track of lyrical ideas and flashes of inspiration?",
        "real_answer": (
            "If I get an idea that's a cool observation or lyric idea, I store it in an "
            "endless swipe file in a notepad app on my phone. I keep a running file of words, "
            "questions, and phrases in my Notes app, searching for the perfect line I wrote "
            "down years earlier. When I'm writing a song, I look through all my lyrics and "
            "cherry-pick ideas that relate to the visual I want to paint. When I'm in my "
            "Notes app scrolling, it looks like I'm just endlessly scrolling, but I'm "
            "scrolling through words in my file."
        ),
    },
    {
        "text": "How do you respond to criticism and use it creatively?",
        "real_answer": (
            "Criticism has been a huge fuel for me — it's been a huge jumping-off point, "
            "like a creative writing prompt or something. Songs like 'Blank Space' wouldn't "
            "exist without criticism about my dating life, and 'Anti-Hero' emerged from being "
            "criticized for aspects of my personality. I loved the Reputation album, and I "
            "was like, 'You guys say what you want. I know what I did. I love it. Go with "
            "God, sorry.' My advice to young artists is: why are you reading your comments? "
            "Write about it. Make art about this. Don't respond to trolls."
        ),
    },
    {
        "text": "How do you approach songwriting collaborations?",
        "real_answer": (
            "I apply one simple rule: may the best idea win. I don't care if it came from "
            "you, you, or me — if it's better, that's what goes in the song. I do kind of "
            "like it when people challenge me on something because it makes the music better. "
            "I never want to be in the room with creators who are afraid that if they have "
            "a better idea they can't argue with me. I love writing sessions because everyone "
            "in the room is bringing ideas and chiming in."
        ),
    },
    {
        "text": "What was your goal with the Eras Tour?",
        "real_answer": (
            "I wanted to superserve the fans to repay them for the effort they put in to "
            "attend my career-retrospective concert. They had to work really hard to get the "
            "tickets, and I wanted to play a show that was longer than they ever thought it "
            "would be. I think about it every day, and I had so much fun on that tour. "
            "My experience and their joy fueled me even when I was exhausted and tired. "
            "The Eras Tour elevated the connection between me and my fans to new heights, "
            "making every fan feel seen, heard, and valued."
        ),
    },
    {
        "text": "What is the concept behind the Midnights album?",
        "real_answer": (
            "I have always been fascinated with sleeplessness — I'm constantly writing about "
            "2am and the middle of the night because I think that's a vulnerable, isolated "
            "time where I have written many of my songs and experienced the catharsis of "
            "songwriting. Midnights is a concept album about nocturnal ruminations inspired "
            "by my sleepless nights. It's autobiographical songwriting that explores broad "
            "emotions such as regrets, self-criticism, fantasies, heartbreak, and infatuation, "
            "using confessional yet cryptic lyrics. The album chronicles 13 sleepless nights "
            "scattered throughout my life."
        ),
    },
    {
        "text": "Do you have any specific technical rules you follow when writing lyrics?",
        "real_answer": (
            "I have this rule where I avoid having a word end with the same letter that the "
            "next word starts with. It changes the rhythm of the line in a way I don't like. "
            "For example, I changed 'talk real low' to 'talk real slow' in one song because "
            "I wanted a different sonic feel. It's these tiny details that matter when you're "
            "crafting lyrics and trying to make them flow perfectly with the melody. Writing "
            "songs takes exacting wordplay and emotional payoff — I obsess over phrasing, "
            "rhythm, and contradiction in my verses."
        ),
    },
]


def seed():
    with Session(engine) as db:
        char = db.query(Character).filter(Character.slug == "taylor-swift").first()
        if not char:
            char = Character(name="Taylor Swift", slug="taylor-swift", created_by="sam")
            db.add(char)
            db.flush()
            print(f"Created character: Taylor Swift (id={char.id})")
        else:
            print(f"Character already exists: Taylor Swift (id={char.id})")

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
