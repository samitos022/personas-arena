"""
Seed script: creates Djo (Joe Keery) character + 10 approved questions with real answers.
Sources: ELLE Dec 2025/Jan 2026, Rolling Stone, NME, Variety, Dork, NYLON, Dazed Digital,
         FLOOD Magazine, Billboard, CBC Arts interviews (2022–2025).
"""
from database import engine
from models import Base, Character, Question
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

QUESTIONS = [
    {
        "text": "Why did you create Djo as a separate identity from your acting work?",
        "real_answer": (
            "Originally, it was to distract from the other stuff I'm known for. "
            "It was a way to disassociate the music. It was pretty much just to deflect "
            "from people being like, 'Hey, Steve!' I wanted to have some sort of separation "
            "between the two so that somebody who wasn't a fan could just discover the music "
            "and listen to it without any preconceived idea of who did it or anything. "
            "Just to have a clean slate. I now realise that if people are coming from the "
            "TV show, and that's the reason that they're finding out about the music? "
            "Hell yeah, that's really cool."
        ),
    },
    {
        "text": "How did you react when 'End of Beginning' went viral on TikTok?",
        "real_answer": (
            "I have literally no idea what's going on. I'm probably more confused than ever, "
            "but it's really, really cool to see something that you've written affect people. "
            "It's pretty unbelievable. You always hope your music finds its place in the world, "
            "and it seems like that one has, in a really big way. I've just stepped back and "
            "watched it take on a life of its own. It was super weird and very intangible — "
            "the strangeness of accidental virality."
        ),
    },
    {
        "text": "What is 'End of Beginning' actually about?",
        "real_answer": (
            "It's about what it means to grow up and look back at a section of your life "
            "and kind of yearn for that. It's about living for the day and not getting too "
            "wrapped up in the past but appreciating it. Going back somewhere, remembering "
            "a time, yearning for it, but also wanting to live in the present. "
            "Turns out that's a very specific thing that is also really common. "
            "In the specificity, people can see themselves in the song. People substitute "
            "my experience for their own version in their own lives."
        ),
    },
    {
        "text": "What was the concept behind the 'Decide' album?",
        "real_answer": (
            "I'm an indecisive person. A lot of change is based around making decisions. "
            "The imagery of the eight-ball is asking the universe, 'What should I do?' "
            "I'd describe it as a sort of aural history of my late 20s — really pessimistic "
            "in some ways, yet also bright and hopeful. Glass half-full or glass half-empty. "
            "David Byrne was a big influence — his gusto and his freedom was something I was "
            "trying to emulate. I like the eclectic nature of it. There are no rules to follow, "
            "so why not really dive into every angle you'd like to explore?"
        ),
    },
    {
        "text": "What's the difference between making music and acting for you?",
        "real_answer": (
            "Really, acting is my main gig. It's the reason I can do other stuff. "
            "But with music, I have a little bit more creative control over the whole vision. "
            "The music is a really good antidote to the fatigue of waiting around for the "
            "acting stuff. I can't just stand up and do my lines to the wall — that's not "
            "really fun. Djo is my version of doing that. It can scratch that creative itch. "
            "They both work so well together because basically, when I'm unemployed and don't "
            "have an acting job, I can do music."
        ),
    },
    {
        "text": "How do you approach songwriting — what's your philosophy?",
        "real_answer": (
            "It's sort of a therapy-style approach, making sense of difficult periods. "
            "I love songs that are really specific — in the specificity, people can see "
            "themselves in the song. The second you censor yourself you start to subtract "
            "the thing that makes it unique to you. If I think something is cool or exciting, "
            "I've got to trust that other people will feel the same way. "
            "Whenever I write a track, there's a hope that it does something magical "
            "for whoever hears it. Music is a direct line to the soul."
        ),
    },
    {
        "text": "How important is humour to your artistic identity?",
        "real_answer": (
            "I realised halfway through recording that maybe humour is part of my identity, "
            "in a lot of things that I do. Why shy away from that? Why not embrace that? "
            "On tour earlier this year, my friends and I were hanging with some of the crew "
            "from the other band, and one of the young ladies said, 'Wow, you guys are not "
            "how I expected you to be.' And I think it was because we were just being silly. "
            "Kind of nerdy. I was a nerdy theater kid, making movies with my friends. "
            "That's deep down who I am."
        ),
    },
    {
        "text": "How did you feel when Stranger Things ended? What was that transition like?",
        "real_answer": (
            "It's kind of a similar thing I was going through when I was looking back at my "
            "time in Chicago. It's like the end of a period of my life. I'm a different person "
            "than I was when I first joined the show. There's a point in everybody's lives "
            "when it's time to spread your wings and move on. It's changing and shifting as "
            "the project goes on. Steve is for the internet; Djo is whatever you want it to be."
        ),
    },
    {
        "text": "Who has inspired you the most in your life?",
        "real_answer": (
            "I've got four sisters. A lot of great cousins, a lot of great aunts. "
            "But I've got to say my mother. She and her friends were unhappy with the education "
            "system in the town I grew up in, and they actually started a charter Montessori "
            "public school. We all went to the school. I was not a traditionally super-talented "
            "academic student — I'd had my troubles. But when I did this sort of off-the-wall "
            "Montessori school until eighth grade, I thrived and loved it. I have a ton of "
            "respect and admiration for her for doing that — she already had a full-time job "
            "raising five kids."
        ),
    },
    {
        "text": "Who is the woman you've worked with who has taught you the most?",
        "real_answer": (
            "The first person who comes to mind is Winona Ryder. I was incredibly intimidated "
            "at first because I grew up on her movies. But as I got to know her, I learned how "
            "invested and passionate she is about work. She really knows her stuff — loves music "
            "and film, maybe more than anyone else in my life. I'll get a random text like, "
            "'Here's an isolated Marvin Gaye vocal track from the stems that they never used "
            "from this song.' The deepest cuts. She's like an encyclopedia, and she's eager "
            "to share. It's cool to have someone who's just really excited by all of this."
        ),
    },
]


def seed():
    with Session(engine) as db:
        char = db.query(Character).filter(Character.slug == "djo").first()
        if not char:
            char = Character(name="Djo (Joe Keery)", slug="djo", created_by="sam")
            db.add(char)
            db.flush()
            print(f"Created character: Djo (Joe Keery) (id={char.id})")
        else:
            print(f"Character already exists: Djo (Joe Keery) (id={char.id})")

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
